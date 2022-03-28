echo ============================================
echo Running Tests
./py-patch -f data/testdata/fakeorbis.elf -c orbistest.yml -v -od
./py-patch -f data/testdata/fakeorbis.elf -c orbistest.yml -v
./py-patch -f data/testdata/fakecell.elf -c celltest.yml -v -od
./py-patch -f data/testdata/fakecell.elf -c celltest.yml -v -o output-file
./py-patch -f data/testdata/fakecell.elf -c celltest.yml -v
./py-patch -f data/testdata/fakecell.elf -c celltest.yml
./py-patch -f data/testdata/testdata.elf -c missingdata.yml -v
echo ============================================
