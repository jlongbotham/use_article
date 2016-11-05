# use_article
Extracts features from CoNLL format for training models on the presence of determiners in a noun phrase.

Usage: `$python extract-features.py [input ConLL] > [output TSV]`

### Example input

```
news-b1597312-98dtest-f72651-s175
Now	now	RB	1	3	Adv
people	people	NNS	2	3	Sb
must	must	MD	3	0	Pred
declare	declare	VB	4	3	Obj
if	if	IN	5	7	AuxC
they	they	PRP	6	7	Sb
collaborated	collaborate	VBD	7	4	Adv
with	with	IN	8	7	AuxP
the	the	DT	9	11	AuxA
secret	secret	JJ	10	11	Atr
services	service	NNS	11	8	Adv
before	before	IN	12	4	AuxP
1990	1990	CD	13	12	Adv
.	.	.	14	0	AuxK
```

### Example output

```
sentence	has_det	has_rel	string	pos_string	head	pos_head	core	pos_core	mod	pos_mod	unigram_pre	pos_unigram_pre	bigram_pre	pos_bigram_pre	trigram_pre	pos_trigram_pre	unigram_post	pos_unigram_post	bigram_post	pos_bigram_post	trigram_post	pos_trigram_post
Now people must declare if they collaborated with the secret services before 1990 . 	False	False	_people_	_NNS_	people	NNS	_people_	_NNS_	_	_	_Now_	_RB_	_BOS_Now_	_BOS_RB_	_BOS_BOS_Now_	_BOS_BOS_RB_	_must_	_MD_	_must_declare_	_MD_VB_	_must_declare_if_	_MD_VB_IN_
Now people must declare if they collaborated with the secret services before 1990 . 	True	False	_secret_service_	_JJ_NNS_	service	NNS	_service_	_NNS_	_secret_	_JJ_	_with_	_IN_	_collaborated_with_	_VBD_IN_	_they_collaborated_with_	_PRP_VBD_IN_	_before_	_IN_	_before_1990_	_IN_CD_	_before_1990_._	_IN_CD_._

```