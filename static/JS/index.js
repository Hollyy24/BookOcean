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

        this.view.searchButton.addEventListener("click", async (event) => {
            event.preventDefault()
            const searchWay = this.view.searchWay.value
            const searchValue = this.view.searchInput.value.trim()
            console.log(searchValue, searchWay)
            if (searchValue) {
                window.location.href = `/search/?way=${searchWay}&value=${searchValue}`;
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
        const books = await this.model.fetchRandomBook();
        if (!books) {
            return
        }
        for (let index in books) {
            this.view.createContent(books[index]);
        }
        document.querySelectorAll(".random-item").forEach(element => {
            element.addEventListener("click", () => {
                const source = element.id.split("/")[0];
                const id = element.id.split("/")[1];
                window.location.href = `/book?source=${source}&id=${id}`;
            })
        })
    }


}

class Model {
    async fetchRandomBook() {
        try {
            const response = await fetch('/api/booksdata', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Fetch error:", error);
            return false
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

    createContent(data) {
        const container = document.querySelector('#random-container');

        let item = document.createElement("div");
        let name = document.createElement("p");
        let img = document.createElement("img");
        let author = document.createElement("p")
        let source = document.createElement('p');
        let url = document.createElement("a");

        item.className = "random-item";
        name.className = "random-name";
        img.className = "random-img";
        author.className = "random-author";
        source.className = 'random-source';
        url.className = 'random-url';
        url.target = "_blank";

        item.title = data.name
        item.id = data.source + "/" + data.id;
        name.textContent = data.name;
        img.src = data.img;
        author.textContent = data.author;
        source.textContent = data.source;
        source.style.backgroundColor = this.sourceColor(data.source);
        url.textContent = "前往購買";
        url.href = data.url;


        item.appendChild(name);
        item.appendChild(img);
        item.appendChild(author);
        item.appendChild(source);
        item.appendChild(url);
        container.appendChild(item)


    }

    sourceColor(source) {
        if (source == "博客來") {
            return "#7ABD54"
        }
        if (source == "誠品") {
            return "#A50034"
        }
        if (source == "三民") {
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




