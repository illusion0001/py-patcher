echo ============================================
echo Running Tests
./py-patch -f data/testdata/fakeorbis.elf -p orbistest.yml -y -v -od
./py-patch -f data/testdata/fakeorbis.elf -p orbistest.yml -y -v
./py-patch -f data/testdata/fakecell.elf -p celltest.yml -y -v -od
./py-patch -f data/testdata/fakecell.elf -p celltest.yml -y -v -o output-folder
./py-patch -f data/testdata/fakecell.elf -p celltest.yml -y -v
./py-patch -f data/testdata/fakecell.elf -p celltest.yml -y
./py-patch -f data/testdata/testdata.elf -p missingdata.yml -y -v
./py-patch -f data/testdata/testdata.elf -p missingdata.yml -y -v -dl
ls -R patch0
echo ============================================
