<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# <center>Introduction to Machine Learning Final Project</center>

<div align="center">

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project">View Demo</a>
    ·
    <a href="https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project/issues">Report Bug</a>
    ·
    <a href="https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project/issues">Request Feature</a>
  </p>
</div>

## Semester and class
2022 Fall NTHU CS 460200

## Introduction
Machine Learning has been prevalent recently. However, instead of the well-known application, such as picture recognition and category prediction, we try to implement a model that can generate bass automatically for jazz music. For instance, Let a piece of jazz music be A + B, B = music of double bass, and A = music played by other instruments (piano, guitar, drums, etc.). We want the model to learn the relationship between A and B. If we input A, the output will be B’. We want B’ to be as similar to B as possible. We then combine B’ and A to get the complete song. Even though it may not seem to be the most lucrative application of Machine Learning compared to some of the most prominent fields of Natural Language Processing (NLP,) Computer Vision, and Quantitative trading, we still see a bright future in the lot of introducing machine learning to music. We use bidirectional LSTM to deal with this task. In addition, we also put some effort into data preprocessing and experiments.

## Built With
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
* ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
* ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!--Badge tips-->
<!--[Badge generater](https://ileriayo.github.io/markdown-badges/)-->
<!--[Simple icons](https://simpleicons.org/)-->
<!--[Make custom icon badges](https://javascript.plainenglish.io/how-to-make-custom-language-badges-for-your-profile-using-shields-io-d2aeaf016b6b)-->

## Requirements

- Python == 3.7 or 3.8
- tensorflow == 2.X (verified working with 2.0 - 2.3, both for CPU and GPU)
- scikit-learn >= 0.20.1
- matplotlib >= 2.2.3

## Models Implemented

- BDLSTM_simple
- bidirectional_LSTM_v2
- bidirectional_RNN_only

## Details about the project

For implementation details, input / output formts, experminents and result, please refer to `Team 40 Final Project Report`.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `license.txt` for more information.

## Contact

[![gmail][gmail]][gmail-url]
<br>
For other contributers, please refer to `Team 40 Final Project Report`.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project.svg?style=for-the-badge
[contributors-url]: https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project/contributors
[forks-shield]: https://img.shields.io/github/forks/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project.svg?style=for-the-badge
[forks-url]: https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project/network/members
[stars-shield]: https://img.shields.io/github/stars/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project.svg?style=for-the-badge
[stars-url]: https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project.svg?style=for-the-badge
[issues-url]: https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project/issues
[license-shield]: https://img.shields.io/github/license/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project.svg?style=for-the-badge
[license-url]: https://github.com/Lewis-Tsai/Introduction-to-Machine-Learning-Final-Project/blob/master/license
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/lewis-tsai-7b570421a

[gmail]: https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white
[gmail-url]: mailto:A38050787@gmail.com
