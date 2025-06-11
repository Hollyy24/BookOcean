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

    }

    async init() {
        const result = await this.model.fetchBookData()
        if (result['success'] == false) {
            alert("發生錯誤！")
            window.location.href = '/'
            return
        }

        this.view.renderData(result['data'],)
        this.view.drawChart(result['priceflow'])

        const status = localStorage.getItem("token");
        const collected = await this.model.Collected(status);
        if (collected) {
            this.view.bookCollectButton.style.display = "none";
            this.view.bookCollected.style.display = "flex";
            this.view.bookCollected.textContent = "於 " + collected + " 收藏";
            return
        }
        this.view.bookCollectButton.addEventListener("click", async () => {
            this.model.addCollection(this.view.bookCollectButton.id)
        }
        )
    }


}

class Model {
    getQueryparameter() {
        const parameter = new URLSearchParams(window.location.search);
        const source = parameter.get('source');
        const id = parameter.get('id');
        const data = {
            "source": source,
            "id": id
        }
        return data
    }
    async fetchBookData() {
        const parameter = this.getQueryparameter()
        try {
            const response = await fetch('/api/booksdetail', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(parameter)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            return false
        }
    }
    async Collected(status) {
        if (!status) { return false }
        const compareData = this.getQueryparameter()
        try {
            const response = await fetch('/api/collect', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "authorization": `Bearer ${status}`
                },
            });
            const data = await response.json();
            for (let book of data['data']) {
                if (book['book_source'] == compareData['source'] && book['book_id'] == compareData['id']) {
                    return book["time"]
                }
            }
            return false;
        } catch (error) {
            return false
        }
    }
    async addCollection(book) {
        const token = localStorage.getItem('token')
        if (!token) {
            alert("請先登入")
            return
        }
        const data = {
            "token": token,
            "book_source": book.split("/")[0],
            "book_id": book.split("/")[1]
        }
        try {
            const response = await fetch('/api/collect', {
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
                window.location.reload()
            }
            if (result["success"] == false) {
                alert("收藏失敗");
            }
            ;
        } catch (error) {
            return
        }
    }
}




class View {
    constructor() {
        this.bookName = document.querySelector('.book-data-name');
        this.bookImg = document.querySelector('.book-data-img');
        this.bookAuthor = document.querySelector('.book-data-author');
        this.bookPublisher = document.querySelector('.book-data-publisher');
        this.bookPublishDate = document.querySelector('.book-data-publish-date');
        this.bookIsbn = document.querySelector('.book-data-isbn');
        this.bookPrice = document.querySelector('.book-data-price');
        this.bookUrl = document.querySelector('.book-data-url');
        this.bookCollectButton = document.querySelector('.book-data-collect');
        this.bookCollected = document.querySelector(".book-collected");
    }

    renderData(data) {
        this.bookName.textContent = data.name;
        this.bookName.href = data.url;
        this.bookAuthor.textContent = data.author;
        this.bookImg.src = data.img;
        this.bookPrice.textContent = data.price;
        this.bookPublishDate.textContent = data.publish_date ? data.publish_date : "----";
        this.bookPublisher.textContent = data.publisher ? data.publisher : "----";
        this.bookIsbn.textContent = data.ISBN ? data.ISBN : "----";
        this.bookUrl.href = data.URL;
        this.bookUrl.target = "_blank";
        this.bookCollectButton.id = data.source + "/" + data.id

    }

    drawChart(price_data) {
        let labels_arry = [];
        let data_array = [];
        for (let index in price_data) {
            labels_arry.push(price_data[index]['time'])
            data_array.push(price_data[index]['price'])
        }
        const ctx = document.getElementById('BooksChart');
        const data = {
            labels: labels_arry,
            datasets: [{
                label: '價格變動',
                data: data_array,
                borderColor: '#37647d;',
                backgroundColor: '#37647d',
                tension: 0.4,           // 曲線平滑度 (0 ~ 1)
                fill: 'while',            // 是否填滿底色
                pointStyle: 'rect',   // 點的樣式（circle、rect、triangle...）
                pointRadius: 5,         // 點的大小
                borderWidth: 5,          // 線的寬度
                stepped: true,               // 是否變成階梯圖
                spanGaps: true,
            }]
        }
        const config = {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#37647d'
                        }
                    },
                    title: {
                        display: true,
                        text: '價格變動',
                        color: '#37647d'
                    },
                    tooltip: {
                        bodyColor: '#37647d',
                        titleColor: '#e34244'
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#37647d'
                        },
                        grid: {
                            color: '#ccc'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#37647d',
                            stepSize: 1,
                            callback: function (value) {
                                return Number.isInteger(value) ? value : '';
                            }
                        },
                        grid: {
                            color: '#ccc'
                        }
                    }
                }
            }
        };

        const myChart = new Chart(ctx, config);
    }
}



