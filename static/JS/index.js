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



        window.addEventListener("loginSuccess", async (e) => {
            document.querySelector("#nav-center").style.display = "none";
            document.querySelector("#nav-right").style.display = "flex";
            const status = localStorage.getItem("token")
            const collected = await this.model.Collected(status)
            document.querySelectorAll(".random-collect").forEach((element) => {
                if (!collected) { return }
                for (let book of collected) {
                    const source = element.id.split("/")[0]
                    const id = element.id.split("/")[1]
                    if (book["book_source"] == source && book["book_id"] == id) {
                        element.textContent = "於" + book["time"] + "收藏";
                        element.style.color = "#37647d";
                        element.style.backgroundColor = "white";
                        element.id = "collected";
                    }
                }
            })
        })

        this.view.searchButton.addEventListener("click", async (event) => {
            event.preventDefault()
            const searchWay = this.view.searchWay.value
            const searchValue = this.view.searchInput.value.trim()
            if (searchValue) {
                window.location.href = `/search?way=${searchWay}&value=${searchValue}`;
            } else {
                alert("請輸入關鍵字");
            }
        })

        this.view.leftButton.addEventListener("click", () => {
            this.view.moveRandom('left');
        })

        this.view.rightButton.addEventListener("click", () => {
            this.view.moveRandom('right');

        })

    }
    async init() {
        const status = localStorage.getItem("token");
        const collected = await this.model.Collected(status)
        const books = await this.model.fetchRandomBook();
        if (!books) {
            return
        }
        for (let index in books) {
            this.view.createContent(books[index], collected);
        }
        document.querySelectorAll(".random-iteminfo").forEach(element => {
            element.addEventListener("click", () => {
                const source = element.id.split("/")[0];
                const id = element.id.split("/")[1];
                window.location.href = `/book?source=${source}&id=${id}`;
            })
        })
        document.querySelectorAll(".random-collect").forEach(button => {
            button.addEventListener("click", async () => {
                if (button.id == "disabled") { return }
                const book = button.id;
                const price = button.dataset.price
                if (book == "collected") {
                    return
                }
                const result = await this.model.addCollection(book, price);
                if (result == true) {
                    button.textContent = "已收藏";
                    button.style.backgroundColor = "white";
                    button.style.color = "#37647d";
                    button.style.cursor = "default";
                    button.id = "collected";

                }
            });
        })
    }


}

class Model {
    async fetchRandomBook() {
        try {
            const response = await fetch('/api/renderbooks', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
            });
            const data = await response.json();
            return data['books'];
        } catch (error) {
            console.error("Fetch error:", error);
            return false
        }
    }
    async Collected(status) {
        if (!status) { return false }
        try {
            const response = await fetch('/api/user/collections', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "authorization": `Bearer ${status}`
                },
            });
            const data = await response.json();
            return data['data'];
        } catch (error) {
            console.error("Fetch error:", error);
            return false
        }
    }

    async addCollection(book, price) {
        const token = localStorage.getItem('token')
        if (!token) {
            alert("請先登入")
            document.querySelector("#dialog-background").style.display = "block";
            document.querySelector("#sign-in-form").style.display = "block";
            return
        }
        if (book == "disabled") { return };
        const data = {
            "book_source": book.split("/")[0],
            "book_price": price,
            "book_id": book.split("/")[1]
        }
        try {
            const response = await fetch('/api/user/collections', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result["success"] == true) {
                alert("收藏成功");
                return true
            }
            if (result["success"] == false) {
                alert("收藏失敗");
                return false
            }
            ;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }


}




class View {
    constructor() {
        this.searchForm = document.querySelector(".searchForm");
        this.searchWay = document.querySelector('.search-category')
        this.searchInput = document.querySelector(".search-input");
        this.searchButton = document.querySelector(".search-button");
        this.leftButton = document.querySelector('.left-button');
        this.rightButton = document.querySelector('.right-button');
    }

    createContent(data, collected) {
        const container = document.querySelector('#random-container');

        let item = document.createElement("div");
        let itemInfo = document.createElement("div");
        let name = document.createElement("p");
        let img = document.createElement("img");
        let author = document.createElement("p")
        let source = document.createElement('p');
        let randomUrlContainer = document.createElement("div");
        let url = document.createElement("a");
        let collect = document.createElement("a");

        item.className = "random-item";
        itemInfo.className = "random-iteminfo";
        name.className = "random-name";
        img.className = "random-img";
        author.className = "random-author";
        source.className = 'random-source';
        randomUrlContainer.className = "random-url-container";
        url.className = 'random-url';
        url.target = "_blank";
        collect.className = "random-collect";

        item.title = data.name
        itemInfo.id = data.source + "/" + data.id;
        name.textContent = data.name;
        img.src = data.img;
        author.textContent = data.author;
        source.textContent = this.sourceName(data.source);
        source.style.backgroundColor = this.sourceColor(data.source);

        url.textContent = "前往購買";
        url.href = data.url;
        collect.id = data.source + "/" + data.id
        collect.dataset.price = data.price
        collect.textContent = "加入收藏"


        itemInfo.appendChild(name);
        itemInfo.appendChild(img);
        itemInfo.appendChild(author);
        itemInfo.appendChild(source);
        item.appendChild(itemInfo);
        item.appendChild(randomUrlContainer)
        randomUrlContainer.appendChild(url);
        randomUrlContainer.appendChild(collect);
        container.appendChild(item)
        if (!collected) { return }
        for (let book of collected) {
            if (data.id == book['book_id'] && data.source == book["book_source"]) {
                collect.style.backgroundColor = "white";
                collect.style.color = "#37647d";
                collect.textContent = "於 " + book["time"] + " 收藏";
                collect.style.cursor = "default";
                collect.id = "collected";
                break;
            }
        }

    }
    sourceName(source) {
        if (source == "books") {
            return "博客來"
        }
        if (source == "eslite") {
            return "誠品"
        }
        if (source == "sanmin") {
            return "三民"
        }
    }

    sourceColor(source) {
        if (source == "books") {
            return "#7ABD54"
        }
        if (source == "eslite") {
            return "#A50034"
        }
        if (source == "sanmin") {
            return "#FFD400"
        }
    }


    moveRandom(path) {
        const container = document.getElementById("random-container");
        const scrollAmount = 200; // 每次滑動距離（px）
        if (path == 'left') {
            container.scrollLeft -= scrollAmount;
        }
        if (path == 'right') {
            container.scrollLeft += scrollAmount;
        }
    }
}




