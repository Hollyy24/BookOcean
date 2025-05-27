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
        this.view.searchButton.addEventListener("click", async (event) => {
            event.preventDefault()
            const bookName = this.view.searchInput.value
            const result = await this.model.fetchData(bookName);
            this.view.esliteContainer.innerHTML = "";
            this.view.bookshopContainer.innerHTML = "";
            if (result["success"] == true) {
                if (result["books"] == "") {
                    alert("查無相關資料")
                    this.view.esliteContainer.innerHTML = "";
                    this.view.bookshopContainer.innerHTML = "";
                    return
                }
                let books = result["books"]
                for (let index in books) {
                    if (books[index].source == "eslite") {
                        this.view.renderResult(books[index], this.view.esliteContainer)
                    } else if (books[index].source == "books") {
                        this.view.renderResult(books[index], this.view.bookshopContainer)
                    }

                    const collectionButtons = document.querySelectorAll('.collect-button');
                    collectionButtons.forEach((element) => {
                        element.onclick = () => {
                            this.model.addCollection(element.id)
                        }
                    })

                }

            }
            if (result["success"] == false) {
                const Message = result["Message"]
                alert(Message)
                return
            }
            return
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

        this.view.siginForm.addEventListener("submit", (event) => {
            event.preventDefault()
            let email = document.querySelector('#sign-in-email').value
            let password = document.querySelector('#sign-in-password').value

            let user = {
                "email": email,
                "password": password
            }
            this.model.userSignin(user)

        })
        this.view.memberCenter.addEventListener("click", () => {
            window.location.href = "/member"
        })

    }
    init() {

        let token = localStorage.getItem('token');
        if (token) {
            this.view.memberCenter.style.display = "block"
            this.view.login.style.display = "none";
            this.view.signin.style.display = "none";

        }
    }
}

class Model {
    async fetchData(bookName) {
        try {
            const response = await fetch('/api/booksdata', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "name": bookName })
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    async userSignin(userData) {
        try {
            const response = await fetch('/api/signinuser', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });
            const result = await response.json();
            if (result["success"] == true) {
                let user = result["userdata"]
                let id = user.id
                localStorage.setItem("token", id)
                alert("登入成功")
                window.location.reload();
            }
            if (result["success"] == false) {
                alert(result["Message"])
            }
            ;
        } catch (error) {
            console.error("Fetch error:", error);
        }

    }

    async userLogin(userData) {
        try {
            const response = await fetch('/api/loginuser', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            });
            const result = await response.json();
            if (result["success"] == true) {
                alert("註冊成功，請重新登入")
                window.location.reload();
            }
            if (result["success"] == false) {
                alert(result["Message"])
            }
            ;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    async addCollection(book_id) {
        const data = {
            "user_id": localStorage.getItem('token'),
            "book_id": book_id
        }
        try {
            const response = await fetch('api/collectbook', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem('token')
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result["success"] == true) {
                alert("收藏成功");
            }
            if (result["success"] == false) {
                alert("收藏失敗");
            }
            ;
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

}




class View {
    constructor() {
        this.homePage = document.querySelector('#nav-title');


        this.login = document.querySelector('#login');
        this.signin = document.querySelector('#signin');
        this.memberCenter = document.querySelector("#member-center");

        this.loginForm = document.querySelector("#log-in-form");
        this.siginForm = document.querySelector("#sign-in-form");
        this.dialogBackground = document.querySelector('#dialog-background');

        this.collectButton = document.querySelector('.collect-button');

    }


    renderResult(data, container, addCollection) {
        this.resultContainer.style.display = "flex";
        this.createContent(data, container, addCollection)
    }

    createContent(data, container) {

        let bookItem = document.createElement("div");
        let bookName = document.createElement("h3");
        let bookImg = document.createElement("img");
        let bookAuthor = document.createElement("p");
        let bookPrice = document.createElement("p");
        let urlContainer = document.createElement("div")
        let bookUrl = document.createElement("a")
        let collectButton = document.createElement("a")

        bookItem.className = "book-item";
        bookName.className = "book-name";
        bookImg.className = "book-img";
        bookAuthor.className = "book-author";
        bookPrice.className = "book-price";
        bookUrl.className = 'book-url';
        bookUrl.target = "_blank";
        urlContainer.className = "url-container";
        collectButton.className = "collect-button";


        bookName.textContent = data.book_name;
        bookImg.src = data.book_img_url;
        bookAuthor.textContent = data.book_author;
        bookPrice.textContent = data.book_price;
        bookUrl.textContent = "前往購買";
        bookUrl.href = data.book_url;
        collectButton.textContent = "加入收藏";
        collectButton.id = data.id;



        bookItem.appendChild(bookName);
        bookItem.appendChild(bookImg);
        bookItem.appendChild(bookAuthor);
        bookItem.appendChild(bookPrice);
        bookItem.appendChild(urlContainer);
        urlContainer.appendChild(bookUrl);
        urlContainer.appendChild(collectButton);
        container.appendChild(bookItem);

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

    setCollectButton() {
        const collectButton = document.querySelectorAll('.collect-book');
        return collectButton
    }
}




