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


        this.view.homePage.addEventListener("click", () => {
            window.location.href = "/"
        })

        this.view.logOut.addEventListener("click", () => {
            this.model.userLogout();
            window.location.href = "/";

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


    }
}

class Model {
    async checkStatus() {
        const token = localStorage.getItem('token')
        if (!token) { return false }
        try {
            const response = await fetch('/api/user', {
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

    userLogout() {
        let token = localStorage.getItem('token');
        localStorage.removeItem('token');
    }
}


class View {
    constructor() {
        this.homePage = document.querySelector('#nav-title');
        this.logOut = document.querySelector('#logout');
        this.profile = document.querySelector("#profile");
        this.profileName = document.querySelector("#profile-name");
        this.profileEmail = document.querySelector("#profile-email");
        this.collectionContainer = document.querySelector("tbody");

    }

    renderProfie(data) {
        this.profileName.textContent = data.name;
        this.profileEmail.textContent = data.email;

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
            bookUrl.href = data[index].url;
            deleteButton.textContent = "刪除"
            colletcTime.textContent = data[index].time;

            urlTd.appendChild(bookUrl)

            // itemContainer.appendChild(collectCheck);
            itemContainer.appendChild(bookName);
            itemContainer.appendChild(bookAuthor);
            itemContainer.appendChild(bookPrice);
            itemContainer.appendChild(urlTd);
            itemContainer.appendChild(colletcTime);
            itemContainer.appendChild(deleteButton);


            this.collectionContainer.appendChild(itemContainer);
        }
    }
}




