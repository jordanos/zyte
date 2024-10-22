
# Scraping Project with Zyte API and Scrapy

This project is designed to scrape **business listings** and their **details** from the [BizBuySell](https://www.bizbuysell.com) website using both the **Zyte API** and **Scrapy**. The project is organized into two parts: 

1. **Zyte API Interaction** - Python code to interact with the Zyte platform through its API.
2. **Scrapy Spider** - A Scrapy project deployed on the Zyte Cloud to scrape the website.

## Folder Structure

The project folder structure looks as follows:

```
root/
├── zyte_api/
│   └── main.py
├── biz/
│   ├── scrapy.cfg
│   ├── scrapinghub.yml
│   └── spiders/
│       └── bsp.py
└── README.md
```

- `zyte_api/` - This folder contains the script `main.py` which uses the **Zyte API** to scrape the BizBuySell website.
- `biz/` - This is a **Scrapy project** that contains a spider named `bsp` to scrape BizBuySell listings. This project is deployed on the Zyte platform using **scrapinghub.yml**, which holds the project ID and configuration.

---

## Getting Started

### Prerequisites

To run this project, you'll need:

- Python 3.7 or higher
- Pip (Python package manager)
- [Zyte API](https://docs.zyte.com/) Key for interacting with the Zyte platform
- [Scrapy](https://scrapy.org/) installed on your local machine

### Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install the required Python packages:
   ```bash
   pip install zyte-api scrapy
   ```

3. Set up your Zyte API key and credentials by exporting it in your environment:
   ```bash
   export ZYTE_API_KEY='your-zyte-api-key'
   ```

---

## Zyte API Scraping (zyte_api)

The Zyte API script is located in the `zyte_api/` folder. This script interacts with Zyte's platform using the `zyte-api` Python library to scrape business listings from BizBuySell.

### Running Zyte API Script

To run the script in `zyte_api/main.py`, use the following command:

```bash
python zyte_api/main.py
```

This script will:
- Connect to the Zyte API using your API key.
- Scrape business listings and details from BizBuySell.

The output of the script will be printed in the console or saved to a file, depending on how you configure it.

---

## Scrapy Project (biz)

The Scrapy project is located in the `biz/` folder. This project contains the spider `bsp` which scrapes the BizBuySell website for business listings and detailed information.

### Scrapy Project Structure

- `biz/spiders/bsp.py` - The spider that handles scraping BizBuySell listings.
- `scrapinghub.yml` - The configuration file that holds your Zyte project ID and deployment settings.

### Running Scrapy Locally

If you want to run the Scrapy spider locally, navigate to the `biz/` directory and run:

```bash
cd biz
scrapy crawl bsp
```

This will execute the `bsp` spider, which scrapes business listings from BizBuySell.

---

## Deployment on Zyte Cloud

### Deploying Scrapy Project

The Scrapy project is set up to be deployed on Zyte Cloud using the `scrapinghub.yml` file, which contains the Zyte project ID.

1. Make sure you have **shub** (ScrapingHub command-line tool) installed:
   ```bash
   pip install shub
   ```

2. Log in to your Zyte account:
   ```bash
   shub login
   ```

3. Deploy the Scrapy project to Zyte Cloud:
   ```bash
   shub deploy
   ```

This will deploy the project to Zyte's infrastructure, and you can schedule and manage spiders from the Zyte dashboard.

---

## Configuration

### Zyte API Key

Make sure your Zyte API key is set correctly by exporting it in your environment:

```bash
export ZYTE_API_KEY='your-zyte-api-key'
```

Alternatively, you can directly pass the API key within the script or configure it in the Zyte dashboard.

### ScrapingHub Project ID

The `scrapinghub.yml` file in the Scrapy project contains the project ID for deployment. Ensure that it looks like this:

```yaml
projects:
  default: 12345/project-id
```

Replace `12345/project-id` with your actual Zyte project ID.

---

## Contribution

Feel free to open a pull request or submit issues if you find any bugs or have suggestions for improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [Zyte](https://zyte.com/) for providing the web scraping platform and API.
- [Scrapy](https://scrapy.org/) for making web scraping with Python easy and powerful.