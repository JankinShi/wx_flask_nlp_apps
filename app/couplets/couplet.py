
from model import Model

m = Model(
        'F:/code/DL/nlp/idiom/wx_idiom/app/couplets/data/train/in.txt',
        'F:/code/DL/nlp/idiom/wx_idiom/app/couplets/data/train/out.txt',
        'F:/code/DL/nlp/idiom/wx_idiom/app/couplets/data/test/in.txt',
        'F:/code/DL/nlp/idiom/wx_idiom/app/couplets/data/test/out.txt',
        'F:/code/DL/nlp/idiom/wx_idiom/app/couplets/data/vocabs.txt',
        num_units=1024, layers=4, dropout=0.2,
        batch_size=32, learning_rate=0.001,
        output_dir='F:/code/DL/nlp/idiom/wx_idiom/app/couplets/output_model/output_couplet',
        restore_model=True)

m.train(start=0,epochs=20)
