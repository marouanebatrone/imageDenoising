# imageDenoising (An image processing web application)

This web application allows users to upload images, apply noise, and then apply various filters to denoise the images. <br>
The application is built using Django for the backend and React for the frontend.

## Features

- Upload an image
- Add different types of noise to the image
- Apply various filters to the noisy image to denoise it
- Store the original, noisy, and filtered images in a database

## Technologies Used

- **Backend**: Django, Django REST framework, OpenCV, Pillow, NumPy, scikit-image
- **Frontend**: React, Material-UI, Axios
- **Database**: MySQL

## Getting Started

### Prerequisites

- Python 3.x
- Node.js
- MySQL

### Setup

1. **Clone the repository:**

   `git clone https://github.com/marouanebatrone/imageDenoising.git` <br>
   `cd imageDenoising`
   
2. **Run the app:**

Run the front end:  <br>
   `cd imageDenoising/imageDenoisingFront` <br>
   `npm install`  <br>
   `npm start`  <br>

Run the back end : <br>

   `cd imageDenoising/imageDenoisingBackEnd` <br>
   `python manage.py runserver`
