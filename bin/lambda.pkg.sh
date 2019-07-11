cd ..
mkdir lambda &&
cp -r src/ lambda &&
pip3 install -Ur requirements.txt -t lambda &&
chmod -R 755 lambda &&
cd lambda
zip -r ../lambda.zip .
cd ..
rm -rf lambda
