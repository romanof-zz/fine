mkdir lambda &&
cp -r src/ lambda &&
pip3 install -U -r requirements.txt -t lambda &&
chmod -R 755 lambda &&
cd lambda
zip -r ../lambda.zip .
cd ..
rm -rf lambda
