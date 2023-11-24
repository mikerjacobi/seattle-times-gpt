REACT_APP_API="https://7begkcdqwg.execute-api.us-west-2.amazonaws.com/prod" npm run build
aws --profile jacobi s3 sync build/ s3://seattle-times-gpt-site
