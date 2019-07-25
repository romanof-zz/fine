cd ..
mkdir lambda &&

echo "== copy sources ==" &&
cp -r src/ lambda &&
chmod -R 755 lambda &&

echo "== copy linux numpy and pandas ==" &&
# download latest from: https://pypi.org/project/numpy/#files
cp bin/numpy-1.16.4-cp37-cp37m-manylinux1_x86_64.whl lambda &&
# download latest from: https://pypi.org/project/pandas/#files
cp bin/pandas-0.25.0-cp37-cp37m-manylinux1_x86_64.whl lambda &&

echo "== install dependencies ==" &&
sudo -H pip3 install -Ur requirements.txt -t lambda &&

cd lambda &&
# @link https://medium.com/@korniichuk/lambda-with-pandas-fd81aa2ff25e
echo "== removing pandas ==" &&
sudo rm -rf pandas &&
echo "== removing numpy ==" &&
sudo rm -rf numpy &&
echo "== removing numpy ==" &&
sudo rm -rf *.dist-info &&

echo "== unpacking numpy & pandas ==" &&
unzip numpy-1.16.4-cp37-cp37m-manylinux1_x86_64.whl &&
unzip pandas-0.25.0-cp37-cp37m-manylinux1_x86_64.whl &&

echo "== cleaning lambda dir before zipping ==" &&
sudo rm -rf *.whl *.dist-info __pycache__ &&

zip -r ../lambda.zip .
cd ..

echo "== removing lambda tmpdir ==" &&
sudo rm -rf lambda
