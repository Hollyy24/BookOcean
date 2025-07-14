window.addEventListener("DOMContentLoaded", function () {
    const model = new Model()
    const view = new View()
    const controller = new Controller(model, view)

})


class Controller {
    constructor(model, view) {
        this.model = model;
        this.view = view;

        this.init(this.view.page)
        this.view.searchButton.addEventListener("click", async (event) => {
            event.preventDefault()
            const searchWay = this.view.searchWay.value
            const searchValue = this.view.searchInput.value.trim()
            if (searchValue) {
                window.location.href = `/search/?way=${searchWay}&value=${searchValue}`;
            } else {
                alert("請輸入關鍵字");
            }
        })

        this.view.searchLeft.addEventListener("click", async () => {
            this.view.page -= 1;
            if (this.view.page < 0) {
                alert("最前頁")
                this.view.page = 0
                return
            }
            const search = this.model.getQueryparameter()
            const data = {
                "way": search.way,
                "value": search.value
            }
            const result = await this.model.fetchData(data, this.view.page * (12))
            if (result == false) {
                alert("發生錯誤，請重新查詢")
                window.location.href = '/'
            }
            if (result["books"].length === 0) {
                this.view.bookText.textContent = "查無相關資料";
                return
            }
            const books = result["books"];
            this.view.bookContainer.textContent = ""
            for (let index in books) {
                this.view.createContent(books[index]);
            }
            document.querySelectorAll(".book-info").forEach(element => {
                element.addEventListener("click", () => {
                    const source = element.id.split("/")[0];
                    const id = element.id.split("/")[1];
                    window.location.href = `/book?source=${source}&id=${id}`;
                });
            });
            document.querySelectorAll(".collect-button").forEach(button => {
                button.addEventListener("click", () => {
                    const book = button.id;
                    this.model.addCollection(book);
                });
            })

        })
        this.view.searchRight.addEventListener("click", async () => {
            this.view.page += 1;
            const search = this.model.getQueryparameter()
            const data = {
                "way": search.way,
                "value": search.value
            }
            const result = await this.model.fetchData(data, (this.view.page * 12))
            if (result == false) {
                alert("發生錯誤，請重新查詢")
                window.location.href = '/'
            }
            if (result["books"].length === 0) {
                alert("資料到底")
                return
            }
            const books = result["books"];
            this.view.bookContainer.textContent = ""
            for (let index in books) {
                this.view.createContent(books[index]);
            }
            document.querySelectorAll(".book-info").forEach(element => {
                element.addEventListener("click", () => {
                    const source = element.id.split("/")[0];
                    const id = element.id.split("/")[1];
                    window.location.href = `/book?source=${source}&id=${id}`;
                });
            });
            document.querySelectorAll(".collect-button").forEach(button => {
                button.addEventListener("click", () => {
                    const book = button.id;
                    this.model.addCollection(book);
                });
            })

        })
    }



    async init(page) {
        const data = this.model.getQueryparameter();
        const result = await this.model.fetchData(data, page);
        if (result == false) {
            alert("發生錯誤，請重新查詢")
            window.location.href = '/'
        }
        if (result["books"].length === 0) {
            this.view.bookText.textContent = "查無相關資料";
            this.view.bookText.style.color = "red";
            return
        }
        const books = result["books"];
        const status = localStorage.getItem("token");
        const collected = await this.model.Collected(status);
        for (let index in books) {
            this.view.createContent(books[index], collected);
        }
        document.querySelectorAll(".book-info").forEach(element => {
            element.addEventListener("click", () => {
                const source = element.id.split("/")[0];
                const id = element.id.split("/")[1];
                window.location.href = `/book?source=${source}&id=${id}`;
            });
        });

        document.querySelectorAll(".collect-button").forEach(button => {
            button.addEventListener("click", async () => {
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
                    button.disable = true;
                }
            });
        })
    }
}

class Model {
    getQueryparameter() {
        const parameter = new URLSearchParams(window.location.search);
        const way = parameter.get('way');
        const value = parameter.get('value');
        const data = {
            "way": way,
            "value": value
        }
        return data
    }


    async fetchData(searchvalue, page) {
        const search_data = {
            "way": searchvalue.way,
            "value": searchvalue.value,
            "page": page
        }
        try {
            const response = await fetch(`/api/books?way=${search_data.way}&value=${search_data.value}&page=${search_data.page}`, {
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
    async Collected(status) {
        if (!status) { return false }
        const compareData = this.getQueryparameter()
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
            return
        }
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
        this.bookText = document.querySelector("#book-text");
        this.collectButton = document.querySelectorAll(".collect-button");
        this.searchForm = document.querySelector(".searchForm");
        this.searchWay = document.querySelector('.search-category')
        this.searchInput = document.querySelector(".search-input");
        this.searchButton = document.querySelector(".search-button");
        this.bookContainer = document.querySelector('.book-container');

        this.page = 0;
        this.searchLeft = document.querySelector(".search-left");
        this.searchRight = document.querySelector(".search-right");

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


    createContent(data, collected) {
        let bookItem = document.createElement("div");
        let bookInfo = document.createElement("div");
        let bookName = document.createElement("h3");
        let bookImg = document.createElement("img");
        let bookAuthor = document.createElement("p");
        let bookPrice = document.createElement("p");
        let bookSource = document.createElement('p');
        let urlContainer = document.createElement("div");
        let bookUrl = document.createElement("a");
        let collectButton = document.createElement("a");

        bookItem.className = "book-item";
        bookInfo.className = "book-info";
        bookName.className = "book-name";
        bookImg.className = "book-img";
        bookAuthor.className = "book-author";
        bookPrice.className = "book-price";
        bookSource.className = 'book-source';
        bookUrl.className = 'book-url';
        bookUrl.target = "_blank";
        urlContainer.className = "url-container";
        collectButton.className = "collect-button";

        bookItem.title = data.name
        bookInfo.id = data.source + "/" + data.id
        bookName.textContent = data.name;
        bookImg.src = data.img;
        bookAuthor.textContent = data.author;
        bookPrice.textContent = data.price + " 元";
        bookSource.textContent = this.sourceName(data.source);
        bookSource.style.backgroundColor = this.sourceColor(data.source);
        bookUrl.textContent = "前往購買";
        bookUrl.href = data.url;
        collectButton.textContent = "加入收藏";
        collectButton.id = `${data.source}/${data.id}`;
        collectButton.dataset.price = data.price;

        urlContainer.appendChild(bookUrl);
        urlContainer.appendChild(collectButton)


        bookInfo.appendChild(bookName);
        bookInfo.appendChild(bookImg);
        bookInfo.appendChild(bookAuthor);
        bookInfo.appendChild(bookPrice);
        bookItem.appendChild(bookSource);
        bookItem.appendChild(bookInfo);
        bookItem.appendChild(urlContainer);
        this.bookContainer.append(bookItem)

        if (!collected) { return }
        for (let book of collected) {
            if (data.id == book['book_id'] && data.source == book["book_source"]) {
                collectButton.style.backgroundColor = "white";
                collectButton.style.color = "#37647d";
                collectButton.textContent = "於 " + book["time"] + " 收藏";
                collectButton.style.cursor = "default";
                collectButton.id = "collected";
                break;
            }
        }


    }

    setCollectButton() {
        const collectButton = document.querySelectorAll('.collect-book');
        return collectButton
    }
}




