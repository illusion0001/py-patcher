echo ============================================
echo Running Tests
python launcher.py -f data/testdata/fakeorbis.elf -c orbistest.yml -v -od
python launcher.py -f data/testdata/fakeorbis.elf -c orbistest.yml -v
python launcher.py -f data/testdata/fakecell.elf -c celltest.yml -v -od
python launcher.py -f data/testdata/fakecell.elf -c celltest.yml -v -o output-file
python launcher.py -f data/testdata/fakecell.elf -c celltest.yml -v
python launcher.py -f data/testdata/fakecell.elf -c celltest.yml
python launcher.py -f data/testdata/testdata.elf -c missingdata.yml -v
echo ============================================
