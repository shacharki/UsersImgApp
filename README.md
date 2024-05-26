# DevOps Final Project: Flask App with Auto Scaling and Load Balancer
## Description
This project demonstrates the implementation of a scalable and resilient Flask web application using AWS services like EC2, S3, Auto Scaling, and a load balancer. The application features user registration, login, and displays user profile images stored in an S3 bucket. It provides a robust foundation for hosting applications that require high availability and scalability.

## Introduction
This document outlines the setup, configuration, and deployment of UsersApp, a Flask web application for user registration and login. The application saves user details in a SQLAlchemy database and displays the image of the connected user from the AWS S3 bucket after successful registration and login. Deployment is done using Docker and AWS EC2, with auto-scaling and load-balancing configurations to ensure high availability and scalability.

## Features
* User registration with password verification
* User login functionality
* Home page displaying all registered users, with logged-in users marked and their picture shown
* Integration with AWS S3 for user picture storage
* Containerization using Docker
* Deployment on AWS EC2 with auto-scaling and load balancing

## Setup Instructions:
### 1. Clone the repository:
* Ensure Docker is installed on your machine. Then, run the following commands:
```bash
git clone https://github.com/shacharki/UsersImgApp.git
cd UsersImgApp
```

### 2. Install Docker and build the Docker image:
```bash
docker build -t usersapp .
docker run -d -p 5000:5000 usersapp
```
### 3. Access the application:
* Open your web browser and navigate to http://localhost:5000.

### 4. Configure Amazon S3:
* Create a private S3 bucket.
* Upload an image file (PNG, JPG, or GIF) that you want to display when the app is running.
* Update the Flask app to use the new S3 bucket name.
* (You can upload an image with public access by creating a public S3 bucket and using the code in the comments in app.py).

<img width="1170" alt="image_private" src="https://github.com/shacharki/UsersImgApp/blob/3d39f067232152a74dc45fa63e9a1f1a9e874d1f/image_private.png">

If you try using the url of the image you will receive this error:
<img width="1170" alt="user_image_private" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/user%20image%20private.png">

## Cloud Computing Setup
### 5. Create an EC2 Instance:
* Launch an EC2 instance.
* Connect to the EC2 instance and run the following commands:
```bash
  sudo yum update -y
  sudo yum install git -y

  sudo yum update -y
  sudo yum install -y docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user

  sudo groupadd docker
  sudo gpasswd -a ec2-user docker
  newgrp docker
```
### 6. Deploy the Application on EC2:
* Follow steps 1-2 above to clone the repository and build the Docker image on the EC2 instance.
* Use the Public IP for the EC2 instance to access the application.

app run on ec2
<img width="1170" alt="app_ru_ec2" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/app%20run%20on%20ec2.png">

### 7. Create an IAM Role:
* Create a new IAM role for EC2 with the `AmazonS3FullAccess` policy attached.
* Assign the `s3ReadOnlyAccess` permission to the instance role.

### 8. Create a Launch Template for EC2:
Create a new launch template with the following settings:
* security groups- Allow inbound traffic on ports 22 (SSH), 80 (HTTP), and 5000 (application).
<img width="1170" alt="security_roles" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/security_roles.png">

* Specify the AMI ID, instance type (t2.micro), key pair, and the IAM role from step 7.
* Add the following user data script to install, clone, and run the app:
```bash
#!/bin/bash

sudo yum update -y
sudo yum install git -y
git clone https://github.com/shacharki/UsersImgApp.git
cd ..
cd ..
cd usersapp/
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker $(whoami)
newgrp docker
docker build -t usersapp .
docker run -d -p 5000:5000 usersapp
```

### 9. Set Up an Auto Scaling Group:
* Create a new Auto Scaling Group using the launch template from step 8.
* Configure the Auto Scaling Group with desired capacity, minimum capacity, and maximum capacity settings.
<img width="1170" alt="asg_details" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/asg_details.png">

### 10. Create a Load Balancer
* Create a new Classic Load Balancer with the following settings:
  - Configure listeners for HTTP on port 80.
  - Add security groups allowing traffic on the necessary ports.
  - Register the EC2 instances in the Auto Scaling Group with the load balancer.
<img width="1170" alt="load_balancer_details" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/load_balancer_details.png">

### 11. Verify Deployment:
* Go to the Target Group in the AWS Management Console and ensure the targets are healthy.
<img width="1170" alt="healfi" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/healfi.png">

* Find the Load Balancer DNS name in the AWS Management Console and navigate to it in your web browser to verify the application is running.
* go to the NLB and find the NLB DNS, copy the DNS to new web browser and see that the app works.

The app, using the load balancer DNS:
<img width="1170" alt="load_balancer_run" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/run%20load%20balancer.png">

#### Simulate Load for Testing Auto Scaling:

* Install `wrk` for load testing:
```bash
brew install wrk
```
Simulate a high number of requests to trigger auto-scaling:
```bash
wrk -t12 -c10000 -d100s http://<load_balancer_dns>
```
<img width="1170" alt="load_balancer_test" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/load_balancer_test">
<img width="1170" alt="load_balancer_instances" src="https://github.com/shacharki/UsersImgApp/blob/dd19743ba7c4560dfbf7165033e6b4937c7f2119/instance%20auto%20scaling.png">

### Notes
* Ensure all AWS resources are properly secured and configured according to best practices.
* Monitor the application and infrastructure for any issues during high load and adjust auto-scaling policies as needed.