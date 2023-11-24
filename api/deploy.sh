export AWS_PROFILE=jacobi
sam build && sam deploy --config-env prod
