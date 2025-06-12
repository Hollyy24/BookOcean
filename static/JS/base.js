window.addEventListener("DOMContentLoaded", function () {
    const model = new BaseModel()
    const view = new BaseView()
    const basecontroller = new BaseController(model, view)

})


class BaseController {
    constructor(model, view) {
        this.model = model;
        this.view = view;

        this.init()

        this.view.homePage.addEventListener("click", () => {
            window.location.href = "/"
        })


        this.view.signin.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeLogin()
            this.view.showSignin()

        })

        this.view.login.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeSignin()
            this.view.showLogin()
        })

        this.view.dialogBackground.addEventListener("click", () => {
            this.view.hideAllForms()

        })

        this.view.changeLogin.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeSignin()
            this.view.showLogin()
        })

        this.view.changeSignin.addEventListener("click", () => {
            this.view.dialogBackground.style.display = "block";
            this.view.closeLogin()
            this.view.showSignin()
        })

        this.view.loginForm.addEventListener("submit", (event) => {
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
        this.view.notificationList.style.width = "300px"
        for (let data of notification) {
            if (data.is_read == false) { count += 1 }
            this.view.renderNotificaiton(data);
        }
        this.view.showNotification(count);
    }
}

class BaseModel {
    async checkStatus() {
        const token = localStorage.getItem('token')
        if (!token) { return false }
        try {
            const response = await fetch('/api/userSignin', {
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
            const response = await fetch('/api/userSignin', {
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
            const response = await fetch('/api/userLogin', {
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
            if (result["data"] == null) {
                return false
            };
            return result['data']
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

}




class BaseView {
    constructor() {
        this.homePage = document.querySelector('#nav-title');
        this.login = document.querySelector('#login');
        this.signin = document.querySelector('#signin');
        this.navCenter = document.querySelector("#nav-center");
        this.navRight = document.querySelector("#nav-right");

        this.memberCenter = document.querySelector("#member-center");

        this.loginForm = document.querySelector("#log-in-form");
        this.siginForm = document.querySelector("#sign-in-form");
        this.dialogBackground = document.querySelector('#dialog-background');

        this.changeSignin = document.querySelector("#change-signin");
        this.changeLogin = document.querySelector("#change-login");

        this.notificationIcon = document.querySelector("#notification-icon");
        this.notificationNumber = document.querySelector("#notification-number");
        this.notificationList = document.querySelector("#notification-list");
        this.notificationContainer = document.querySelector("#notification-container");
        this.notificationLeave = document.querySelector("#notification-leave");
    }
    showLogin() {
        this.loginForm.style.display = "block";
    }

    showSignin() {
        this.siginForm.style.display = "block";
    }

    closeSignin() {
        this.siginForm.style.display = "none";
    }
    closeLogin() {
        this.loginForm.style.display = "none";
    }

    hideAllForms() {
        this.closeSignin();
        this.closeLogin();
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

        item.className = "notification-item";
        content.className = "notification-content";
        time.className = "notification-time";


        let text = `
            你收藏的書本 
            『${data.name} 價格已變動』
            前次價格 ${data.old_price} 元
            現在價格 ${data.new_price} 元 
            `;
        content.textContent = text;
        time.textContent = data.time;
        if (data.is_read == false) {
            item.style.opacity = "0.8";
        }

        item.addEventListener("click", async () => {
            const response = await fetch(`/api/notification/${data.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ is_read: true })
            });
            const result = await response.json()
            if (result["success"] == true) { window.location.href = `/book?source=${data.book_source}&id=${data.book_id}`; }
        });

        item.appendChild(content)
        item.appendChild(time);
        this.notificationList.append(item)
    }
}


