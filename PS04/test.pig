A = load 'test.txt';
B = foreach A generate flatten(TOKENIZE((chararray)$0)) as word;
new_B = foreach B generate LOWER(word) as low_word;
--e_start = FILTER new_B BY STARTWITH(low_word,'h') as e_word;
e_start = FILTER new_B BY (low_word MATCHES '^e.*');
C = group e_start by low_word;
D = foreach C generate COUNT(e_start), group;
DUMP D;
