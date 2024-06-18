### How to deploy to AWS

1. You need the private key to access the EC2 instance.
2. Run the deploy playbook via ansible:

```bash
$ ansible-playbook -i "<AWS_MACHINE_IP>," ./prod/play-deploy.yml --private-key <key-location.pem> -u ubuntu
```

3. Enjoy
