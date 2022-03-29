echo ============================================
echo Running Tests
python launcher.py -f data/testdata/fakeorbis.elf -p orbistest.yml -y -v -od
python launcher.py -f data/testdata/fakeorbis.elf -p orbistest.yml -y -v
python launcher.py -f data/testdata/fakecell.elf -p celltest.yml -y -v -od
python launcher.py -f data/testdata/fakecell.elf -p celltest.yml -y -v -o output-folder
python launcher.py -f data/testdata/fakecell.elf -p celltest.yml -y -v
python launcher.py -f data/testdata/fakecell.elf -p celltest.yml -y
python launcher.py -f data/testdata/testdata.elf -p missingdata.yml -y -v
echo ============================================
