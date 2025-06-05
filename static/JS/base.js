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
    async init() {
        const result = await this.model.checkStatus()
        if (result == false) { return }
        this.view.memberCenter.style.display = "block"
        this.view.login.style.display = "none";
        this.view.signin.style.display = "none";

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

}




class BaseView {
    constructor() {
        this.homePage = document.querySelector('#nav-title');
        this.login = document.querySelector('#login');
        this.signin = document.querySelector('#signin');
        this.memberCenter = document.querySelector("#member-center");

        this.loginForm = document.querySelector("#log-in-form");
        this.siginForm = document.querySelector("#sign-in-form");
        this.dialogBackground = document.querySelector('#dialog-background');

        this.changeSignin = document.querySelector("#change-signin");
        this.changeLogin = document.querySelector("#change-login");

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

}


