<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br/>
<div align="center">
  <a href="https://github.com/GonzaloAltatec/CamLink">
    <img src="logo.webp" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">CamLink</h3>

  <p align="center">
    Automated tool for configuration and revision of CCTV devices
    <br />
    <a href="https://github.com/GonzaloAltatec/CamLink"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/GonzaloAltatec/CamLink">View Demo</a>
    ·
    <a href="https://github.com/GonzaloAltatec/CamLink/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/GonzaloAltatec/CamLink/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <ul>
            <li><a href="#docker">Docker</a></li>
            <ul>
                <li><a href="#debian">Debian</a></li>
                <li><a href="#fedora">Fedora</a></li>
            </ul>
        </ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <ul>
    <li><a href="#python-3.12">Python 3.12</a></li>
            <ul>
                <li><a href="#debian">Debian</a></li>
                <li><a href="#fedora">Fedora</a></li>
            </ul>
    </ul>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

<p>Project made by Altatec Seguridad.</p>
<p>The project is a Rest API designed to be mounted on a business environment server. The API waits to receive an ID of an element registered in the internal DB of the ERP.</p>
<p>The received element should contain data of a CCTV model such as security cameras. Actually the API is able to comunicate with Hikvisio ISAPI based devices in order to check it's configurations and change parameters remotely.</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
# Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

## Prerequisites

<p>Follow the steps to install project dependencies.</p>

<!-- DOCKER INSTALL -->
### Docker
<!-- Debian -->
* <b>Debian</b>

1. Set up Docker <code>apt</code> repository:

    ```sh
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    
    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

2. Install Docker package:

    ```sh
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

3. Verify Installation:

    ```sh
    sudo docker run hello-world
    ```

<!-- Fedora -->
* <b>Fedora</b>

1. Install <code>dnf-plugins-core</code> package:

    ```sh
    sudo dnf -y install dnf-plugins-core
    sudo dnf-3 config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
    ```

2. Install Docker Engine:

    ```sh
    sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

3. Start Docker:

    ```sh
    sudo systemctl start docker
    ```

3. Verify Installation:

    ```sh
    sudo docker run hello-world
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

### Enviroment

<p> This project uses dotenv library to use envoriment vatiables nedeet to ensure the correct comunication wit Odoo ERP. To run the program correctly you must create <code>.env</code> file on root directory and write the following variables:</p>

<p>URL='<code>erp_url</code>'</p>
<p>DB='<code>db_url</code>'</p>
<p>USERNAME='<code>username</code>'</p>
<p>PASSWORD='<code>password</code>'</p>

<hr>

### Docker

1. <b>Clone the repo</b>

   ```sh
   git clone https://github.com/GonzaloAltatec/CamLink.git
   ```

2. <b>Acess repo directory</b>

   ```sh
   cd CamLink
   ```

3. <b>Build Docker image</b>

   ```sh
   docker build -t camlink .
   ```

4. <b>Run Docker container</b>

   ```sh
   docker run -p8000:<your_port> camlink
   ```

5. <b>Stop Docker Container</b>

    <p> To stop the container you have to list the running images. </p>

    ```sh
    docker ps -a
    ```

    <p> Once you list the running containers copy the container ID and execute: </p>

    ```sh
    docker rm <container_id>
    ```

6. <b>(Optional) Detached mode & Logs</b>

    <p> If you want to run Docker container on "Detached mode" run the following command: </p>

   ```sh
   docker run -d -p8000:<your_port> camlink
   ```

   <p> Once if you run the container on detached mode the container will run on the background, but if you want to see the logs and console information run this command: </p>

    ```sh
    docker logs <container_id>
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

* [x] Revise devices
* [ ] MongoDB migration
* [ ] Configure devices
* [ ] Kubernetes implementation

See the [open issues](https://github.com/GonzaloAltatec/CamLink/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<br>

<p> Project it's written in Python 3.12 version, if you want to execute source code to test without building the docker image, please read the following Python 3.12 installation guide. </p>

<!-- PYTHON-3.12 INSTALL -->
### Python-3.12 Installation
<!-- Debian -->
* <b>Debian</b>

1. Update system:

    ```sh
    sudo apt update -y
    sudo apt upgrade -y
    ```

2. Install dependencies:

    ```sh
    sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
    ```

3. Download source code:

    ```sh
    wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
    ```

4. Extract files:

    ```sh
    tar -xf Python-3.12.0.tgz
    ```

5. Configure and build:

    ```sh
    cd Python-3.12.0
    ./configure --enable-optimizations
    ```

6. Build Python:

    ```sh
    make -j 4
    ```

7. Install:

    ```sh
    sudo make altinstall
    ```

    <small><i>Using altinstall instead of install prevents it from replacing the system's default Python interpreter (which could cause system tools to malfunction).</i></small>

8. Verify Installation:

    ```sh
    python3.12 --version
    ```

<!-- Fedora -->
* <b>Fedora</b>

1. Update system:

    ```sh
    sudo dnf update
    ```

2. Install dependencies:

    ```sh
    sudo dnf groupinstall 'Development Tools'
    sudo dnf install openssl-devel bzip2-devel libffi-devel sqlite-devel 
    ```

3. Download source code:

    ```sh
    wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
    ```

4. Extract files:

    ```sh
    tar -xf Python-3.12.0.tgz
    ```

5. Configure and build:

    ```sh
    cd Python-3.12.0
    ./configure --enable-optimizations
    ```

6. Build Python:

    ```sh
    make -j 4
    ```

7. Install:

    ```sh
    sudo make altinstall
    ```

    <small><i>Using altinstall instead of install prevents it from replacing the system's default Python interpreter (which could cause system tools to malfunction).</i></small>

8. Verify Installation:

    ```sh
    python3.12 --version
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors

<a href="https://github.com/GonzaloAltatec/CamLink/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=GonzaloAltatec/CamLink" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Gonzalo Rodríguez - <gonzalorodriguez@altatec-seguridad.com>

Project Link: [https://github.com/GonzaloAltatec/CamLink](https://github.com/GonzaloAltatece/CamLink)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/GonzaloAltatec/CamLink.svg?style=for-the-badge
[contributors-url]: https://github.com/GonzaloAltatec/CamLink/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GonzaloAltatec/CamLink.svg?style=for-the-badge
[forks-url]: https://github.com/GonzaloAltatec/CamLink/network/members
[stars-shield]: https://img.shields.io/github/stars/GonzaloAltatec/CamLink.svg?style=for-the-badge
[stars-url]: https://github.com/GonzaloAltatec/CamLink/stargazers
[issues-shield]: https://img.shields.io/github/issues/GonzaloAltatec/CamLink.svg?style=for-the-badge
[issues-url]: https://github.com/GonzaloAltatec/CamLink/issues
[license-shield]: https://img.shields.io/github/license/GonzaloAltatec/CamLink.svg?style=for-the-badge
[license-url]: https://github.com/GonzaloAltatec/CamLink/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastApi-url]: https://fastapi.tiangolo.com/
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
