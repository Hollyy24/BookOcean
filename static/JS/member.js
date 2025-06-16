window.addEventListener("DOMContentLoaded", function () {
    const model = new Model()
    const view = new View()
    const controller = new Controller(model, view)

})


class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;
        this.init()

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

        this.view.logOut.addEventListener("click", () => {
            this.model.userLogout();
            window.location.href = "/";

        })

        this.view.imgOpen.addEventListener("click", () => {
            this.view.dialog.showModal();
        })

        this.view.imgCancle.addEventListener("click", () => {
            this.view.dialog.close();
        })

        this.view.uploadButton.addEventListener("click", async (event) => {
            event.preventDefault();
            const name = this.view.uploadName.value;
            const password = this.view.uploadPassword.value;
            if (!name || !password) {
                alert("欄位不得空白")
                return
            }
            const result = await this.model.uploadMemberdata(name, password);
            if (result["success"] == false) {
                alert("更新失敗！")
                return
            }
            alert("更新成功")
            localStorage.setItem("token", result["data"])
            window.location.reload()
        })

        this.view.imgFile.addEventListener('change', function () {
            const file = this.files[0];
            const maxSize = 2 * 1024 * 1024;
            if (file && file.size >= maxSize) {
                alert("檔案大小不得超過 2MB！");
                this.value = "";
            }
        });


        this.view.imgUpload.addEventListener("click", async () => {
            const file = this.view.imgFile.files[0];
            if (!file) {
                alert("未上傳檔案");
                return
            }
            const result = await this.model.uploadImage(file)
            console.log(result)
            if (result == true) {
                window.location.reload();
            }
        })

        this.view.notificationIcon.addEventListener("click", (element) => {
            this.view.notificationList.style.display = "block";

        })

        this.view.notificationLeave.addEventListener("click", async (event) => {
            this.view.notificationList.style.display = "none";
        })


    }

    async init() {
        let token = localStorage.getItem('token');
        if (!token) {
            window.location.href = "/";
        }
        const member = await this.model.checkStatus()
        this.view.renderProfie(member);

        const result = await this.model.getCollection();
        if (result["success"] == false) { return }
        this.view.createCollect(result["data"])

        document.querySelectorAll('.collect-delete').forEach((element) => {
            element.addEventListener("click", async () => {
                const result = await this.model.delteCollection(element.dataset.id, element.dataset.source)
                console.log(result)
                if (result["success"] == true) {
                    alert("刪除成功")
                    window.location.reload()
                } else if (result["success"] == false)
                    alert("刪除失敗")
            })
        })

        const notification = await this.model.fetchNotification()
        let count = 0;
        if (!notification) { return }
        if (notification.length != 0) {
            this.view.notificationList.style.width = "300px"
        }
        for (let data of notification) {
            if (data.is_read == false) { count += 1 }
            this.view.notificationContainer.textContent = "";
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

        this.ws = new WebSocket(`ws://${location.host}/ws/${this.tempToken}`);

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

class Model {
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
            const member = result["data"];
            return member
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }
    async getCollection() {
        try {
            let token = localStorage.getItem('token')
            const response = await fetch('/api/collect', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `Bearer ${token}`,
                }
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    async delteCollection(id, source) {
        const token = localStorage.getItem('token')
        try {
            const response = await fetch('/api/collect', {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    book_id: id,
                    book_source: source
                })
            });
            const result = await response.json();
            return result;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    async uploadMemberdata(name, password) {
        const token = localStorage.getItem('token')
        try {
            const response = await fetch('/api/userSignin', {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    "name": name,
                    "password": password
                })
            });
            const result = await response.json();
            return result;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    async uploadImage(file) {
        const token = localStorage.getItem('token')
        const formData = new FormData();
        formData.append("file", file);
        const response = await fetch(
            "/api/uploads", {
            method: "POST",
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData
        })

        if (response['success'] == false) {
            return false;
        }
        return true;
    }
    userLogout() {
        let token = localStorage.getItem('token');
        localStorage.removeItem('token');
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
            if (result["success"] == false) { return false };
            const notification = result["data"];
            return notification
        } catch (error) {
            return false
        }
    }
    getTempToken() {
        let tempToken = localStorage.getItem("tempToken");
        if (!tempToken) {
            tempToken = crypto.randomUUID;
            localStorage.setItem("tempToken", tempToken);
        }
        return tempToken;
    }
}


class View {
    constructor() {
        this.homePage = document.querySelector('#nav-title');
        this.logOut = document.querySelector('#logout');
        this.profile = document.querySelector("#profile");
        this.profileName = document.querySelector("#profile-name");
        this.profileEmail = document.querySelector("#profile-email");
        this.profileImg = document.querySelector("#profile-img");
        this.collectionContainer = document.querySelector("tbody");
        this.dialog = document.querySelector("#img-dialog");
        this.imgOpen = document.querySelector("#img-open");
        this.imgUpload = document.querySelector("#img-upload");
        this.imgCancle = document.querySelector("#img-cancle");
        this.imgFile = document.querySelector("#img-input");

        this.uploadName = document.querySelector("#update-form-name")
        this.uploadPassword = document.querySelector("#update-form-password")
        this.uploadButton = document.querySelector("#update-form-button")

        this.notificationIcon = document.querySelector(".notification-icon");
        this.notificationNumber = document.querySelector(".notification-number");
        this.notificationList = document.querySelector(".notification-list");
        this.notificationContainer = document.querySelector(".notification-container");
        this.notificationLeave = document.querySelector(".notification-leave");

    }

    renderProfie(data) {
        this.profileName.textContent = data.name;
        this.profileEmail.textContent = data.email;
        if (data.img) {
            this.profileImg.style.backgroundImage = `url(${data.img})`;
        }

    }

    createCollect(data) {
        for (let index in data) {
            let itemContainer = document.createElement("tr");
            let collectCheck = document.createElement("tb");
            let bookName = document.createElement("td");
            let bookAuthor = document.createElement("td");
            let bookPrice = document.createElement("td");
            let urlTd = document.createElement("td");
            let bookUrl = document.createElement("a");
            let colletcTime = document.createElement("td");
            let deleteButton = document.createElement("td");

            collectCheck.className = "collect-check";
            itemContainer.className = "collect-container";
            bookName.className = "collecct-name";
            bookAuthor.className = "collect-author";
            bookPrice.className = "collect-price";
            urlTd.className = "collect-url";
            colletcTime.className = 'collect-time';
            deleteButton.className = 'collect-delete';
            deleteButton.dataset.id = data[index].book_id;
            deleteButton.dataset.source = data[index].book_source;

            itemContainer.id = data[index].book_id;
            collectCheck.innerHTML = '<input type="checkbox" name="collect-check">'
            bookName.textContent = data[index].name;
            bookAuthor.textContent = data[index].author;
            bookPrice.textContent = data[index].price;
            bookUrl.textContent = "連結"
            bookUrl.target = "_blank"
            bookUrl.href = data[index].url;
            deleteButton.textContent = "刪除"
            colletcTime.textContent = data[index].time;

            urlTd.appendChild(bookUrl)

            itemContainer.appendChild(bookName);
            itemContainer.appendChild(bookAuthor);
            itemContainer.appendChild(bookPrice);
            itemContainer.appendChild(urlTd);
            itemContainer.appendChild(colletcTime);
            itemContainer.appendChild(deleteButton);


            this.collectionContainer.appendChild(itemContainer);
        }
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
    updateOnlineCount(count) {
        const counter = document.getElementById("online-count");
        if (counter) {
            counter.textContent = count;
        }
    }
}




