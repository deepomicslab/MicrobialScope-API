import gzip
import time

# 确认路径（替换为你实际的路径）
file_path = "./Acanthochromis_polyacanthus.ASM210954v1.dna.nonchromosomal.fa.gz"


def read_fasta_gz(file_path):
    with gzip.open(file_path, 'rt') as f:
        header = None
        sequence = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    yield header, ''.join(sequence)
                header = line
                sequence = []
            else:
                sequence.append(line)
        if header:
            yield header, ''.join(sequence)


if __name__ == '__main__':
    start = time.time()
    for header, seq in read_fasta_gz(file_path):
        print(header)
        print(len(seq))

    end = time.time()
    print(f'Read sequences in {end - start:.2f} seconds')
