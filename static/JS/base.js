window.addEventListener("DOMContentLoaded", function () {
    const model = new BaseModel()
    const view = new BaseView()
    const basecontroller = new BaseController(model, view)

})


class BaseController {
    constructor(model, view) {
        this.model = model;
        this.view = view;

        this.channel = new BroadcastChannel("bookocean_online_channel");
        this.ws = null;
        this.connected = false;
        this.shouldConnect = true;

        this.tempToken = this.model.getTempToken();

        this.init();
        this.setupBroadcastChannel();
        this.connectWebSocket();

        document.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "visible" && !this.connected) {
                setTimeout(this.connectWebSocket, 200);
            }
        });

        window.addEventListener("beforeunload", () => {
            if (this.connected) {
                this.channel.postMessage("disconnected");
            }
        });

        this.view.homePage.addEventListener("click", () => {
            window.location.href = "/"
        })


        this.view.signin.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeSignup()
            this.view.showSignin()

        })

        this.view.signup.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeSignin()
            this.view.showSignup()
        })

        this.view.dialogBackground.addEventListener("click", () => {
            this.view.hideAllForms()

        })

        this.view.changeSignup.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeSignin()
            this.view.showSignup()
        })

        this.view.changeSignin.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeSignup()
            this.view.showSignin()
        })

        this.view.signupForm.addEventListener("submit", (event) => {
            event.preventDefault()
            let name = document.querySelector('#log-in-name').value
            let email = document.querySelector('#log-in-email').value
            let password = document.querySelector('#log-in-password').value

            let user = {
                "name": name,
                "email": email,
                "password": password
            }
            this.model.userLogin(user)

        })
        this.view.notificationIcon.addEventListener("click", (element) => {
            this.view.notificationList.style.display = "block";

        })

        this.view.notificationLeave.addEventListener("click", async (event) => {
            this.view.notificationList.style.display = "none";
        })


        this.view.siginForm.addEventListener("submit", async (event) => {
            event.preventDefault()
            let email = document.querySelector('#sign-in-email').value
            let password = document.querySelector('#sign-in-password').value

            let user = {
                "email": email,
                "password": password
            }
            const result = await this.model.userSignin(user)
            if (result == true) {
                this.model.updateUIAfterSignin();
            }


        })
        this.view.memberCenter.addEventListener("click", () => {
            window.location.href = "/member"
        })

    }
    async init() {
        const result = await this.model.checkStatus()
        if (result == false) {
            this.view.navRight.style.display = "none";
            this.view.navCenter.style.display = "flex"
            return
        }
        this.view.navRight.style.display = "flex";
        this.view.navCenter.style.display = "none"


        const notification = await this.model.fetchNotification()
        let count = 0;
        if (!notification) { return }
        this.view.notificationContainer.textContent = "";
        this.view.notificationList.style.width = "300px"
        for (let data of notification) {
            if (data.is_read == false) { count += 1 }
            this.view.renderNotificaiton(data);
        }
        this.view.showNotification(count);
    }
    setupBroadcastChannel() {
        this.channel.onmessage = (msg) => {
            if (msg.data === "already-connected") {
                this.shouldConnect = false;
                if (this.ws && this.connected) this.ws.close();
            }
            if (msg.data === "disconnected") {
                setTimeout(() => {
                    if (!this.connected) this.connectWebSocket();
                }, 200);
            }
            if (msg.data.type === "update-count") {
                this.view.updateOnlineCount(msg.data.count);
            }
        };
    }
    connectWebSocket() {
        if (!this.shouldConnect || this.connected) return;
        const protocol = location.protocol === "https:" ? "wss" : "ws";
        this.ws = new WebSocket(`${protocol}://${location.host}/ws/${this.tempToken}`);
        this.ws.onopen = () => {
            this.connected = true;
            this.channel.postMessage("already-connected");
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.view.updateOnlineCount(data.count);
            this.channel.postMessage({ type: "update-count", count: data.count });
        };

        this.ws.onclose = () => {
            this.connected = false;
            this.channel.postMessage("disconnected");
        };
    }
}

class BaseModel {
    async checkStatus() {
        const token = localStorage.getItem('token')
        if (!token) { return false }
        try {
            const response = await fetch('/api/user/login', {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
            })
            const result = await response.json();
            if (result["success"] == false) { return false };
            const member = result["memberdata"];
            return member
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    async userSignin(userData) {
        try {
            const response = await fetch('/api/user/login', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });
            const result = await response.json();
            if (result["success"] == true) {
                const token = result["memberdata"]
                localStorage.setItem("token", token)
                alert("登入成功")
                return true
            }
            if (result["success"] == false) {
                alert(result["Message"])
                return false

            }
            ;
        } catch (error) {
            console.error("Fetch error:", error);
        }

    }

    async userLogin(userData) {
        try {
            const response = await fetch('/api/user/signup', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });
            const result = await response.json();
            if (result["success"] == true) {
                alert("註冊成功，請重新登入")
            }
            if (result["success"] == false) {
                alert(result["Message"])
            }
            ;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    async fetchNotification() {
        const token = localStorage.getItem('token')
        if (!token) { return false }
        try {
            const response = await fetch('/api/notification', {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            })
            const result = await response.json();
            if (result["success"] == false) {
                return false
            };
            return result['data']
        } catch (error) {
            return false
        }
    }

    async removeNotification(notification_id) {
        try {
            const response = await fetch(`/api/notification/${notification_id}`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            })
            const result = await response.json();
            if (result["success"] == false) {
                return false
            };
            return true
        } catch (error) {
            return false
        }
    }


    updateUIAfterSignin() {
        document.querySelector("#dialog-background").style.display = "none";
        document.querySelector("#sign-in-form").style.display = "none";
        document.querySelector("#login").style.display = "none";
        document.querySelector("#signin").style.display = "none";
        document.querySelector("#member-center").style.display = "flex";

        const event = new CustomEvent("loginSuccess", {
            detail: { reload: "reload" }
        });
        window.dispatchEvent(event);
    }
    getTempToken() {
        let tempToken = localStorage.getItem("tempToken");
        if (!tempToken) {
            tempToken = crypto.randomUUID();
            localStorage.setItem("tempToken", tempToken);
        }
        return tempToken;
    }
}




class BaseView {
    constructor() {
        this.homePage = document.querySelector('#nav-title');
        this.signup = document.querySelector('#signup');
        this.signin = document.querySelector('#signin');
        this.navCenter = document.querySelector("#nav-center");
        this.navRight = document.querySelector("#nav-right");

        this.memberCenter = document.querySelector("#member-center");

        this.signupForm = document.querySelector("#sign-up-form");
        this.siginForm = document.querySelector("#sign-in-form");
        this.dialogBackground = document.querySelector('#dialog-background');

        this.changeSignin = document.querySelector("#change-signin");
        this.changeSignup = document.querySelector("#change-signup");

        this.notificationIcon = document.querySelector(".notification-icon");
        this.notificationNumber = document.querySelector(".notification-number");
        this.notificationList = document.querySelector(".notification-list");
        this.notificationContainer = document.querySelector(".notification-container");
        this.notificationLeave = document.querySelector(".notification-leave");
    }
    showSignup() {
        this.signupForm.style.display = "block";
    }

    showSignin() {
        this.siginForm.style.display = "block";
    }

    closeSignin() {
        this.siginForm.style.display = "none";
    }
    closeSignup() {
        this.signupForm.style.display = "none";
    }

    hideAllForms() {
        this.closeSignin();
        this.closeSignup();
        this.dialogBackground.style.display = "none";
    }

    showNotification(count) {
        if (count == 0) { return }
        this.notificationNumber.textContent = count;
        this.notificationNumber.style.display = "block";
    }
    renderNotificaiton(data) {

        let item = document.createElement("div");
        let content = document.createElement("p");
        let time = document.createElement("p");
        let deleteButton = document.createElement("div");

        item.className = "notification-item";
        content.className = "notification-content";
        time.className = "notification-time";
        deleteButton.className = "notification-delete";

        let text = `
            你收藏的書本 
            『${data.name} 價格已變動』
            前次價格 ${data.old_price} 元
            現在價格 ${data.new_price} 元 
            `;
        content.textContent = text;
        time.textContent = data.time;
        deleteButton.textContent = " ✖ "
        deleteButton.dataset.id = data.id

        if (data.is_read == false) {
            item.style.opacity = "0.8";
        }

        content.addEventListener("click", async () => {
            const response = await fetch(`/api/notification/${data.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ is_read: true })
            });
            const result = await response.json()
            if (result["success"] == true) { window.location.href = `/book?source=${data.book_source}&id=${data.book_id}`; }
        });

        deleteButton.addEventListener("click", async () => {
            const response = await fetch(`/api/notification/${data.id}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
            });
            const result = await response.json()
            if (result["success"] == true) { window.location.reload(); }
        });

        item.appendChild(deleteButton);
        item.appendChild(content);
        item.appendChild(time);
        this.notificationList.append(item)
    }
    updateOnlineCount(count) {
        const counter = document.getElementById("online-count");
        if (counter) {
            counter.textContent = count;
        }
    }
}


