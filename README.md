# BookOcean
![icon](docs/bookocean.png)

Welcome to **BookOcean** 

a website that helps you find  the prices of books from different book shops!

This project automatically crawls book data from online bookstores and helps users track book prices and get notified when prices change.

DEMO website : https://interestingthing4all.fit

## Features

- Search books by title or author with Chinese word segmentation (Jieba)
- Find the most relevant result and display its price
- Add favorite books and receive price drop notifications
- Daily auto-update using scheduled crawler
- Track price history over time


## Architecture

![Architecture](<docs/architecture .png>)

## ERD

![ERD ](./docs/ERD.png)


## Built With

### FrontEnd
- HTML
- CSS
- JavaScript

### BackEnd
- Python
- FastAPI

### Version Control
- Git

### Deployment & Infrastructure
- Docker
- GitHub
  - Git Action Deploy   
- AWS
  - EC2
  - S3
  - CloudFront
  - RDS (MySQL)
- Nginx



## Disclaimer
This project is for educational and demonstrational purposes only and is not intended for commercial use. All data crawled belongs to the original websites. Users should comply with the terms of service of the respective websites. The author is not responsible for any legal issues arising from improper use.



