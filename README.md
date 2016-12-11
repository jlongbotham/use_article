# use_article
Extracts features from CoNLL format for training models on the presence of determiners in a noun phrase.

Usage: `$python extract-features.py [input ConLL] [corpus czeng or ontonotes]> [output TSV]`

### Example CzEng input

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

### Example CzEng output

```
sentence	has_det	has_rel	string	pos_string	head	pos_head	core	pos_core	mod	pos_mod	unigram_pre	pos_unigram_pre	bigram_pre	pos_bigram_pre	trigram_pre	pos_trigram_pre	unigram_post	pos_unigram_post	bigram_post	pos_bigram_post	trigram_post	pos_trigram_post
Now people must declare if they collaborated with the secret services before 1990 . 	False	False	_people_	_NNS_	people	NNS	_people_	_NNS_	_	_	_Now_	_RB_	_BOS_Now_	_BOS_RB_	_BOS_BOS_Now_	_BOS_BOS_RB_	_must_	_MD_	_must_declare_	_MD_VB_	_must_declare_if_	_MD_VB_IN_
Now people must declare if they collaborated with the secret services before 1990 . 	True	False	_secret_service_	_JJ_NNS_	service	NNS	_service_	_NNS_	_secret_	_JJ_	_with_	_IN_	_collaborated_with_	_VBD_IN_	_they_collaborated_with_	_PRP_VBD_IN_	_before_	_IN_	_before_1990_	_IN_CD_	_before_1990_._	_IN_CD_._

```

### Example OntoNotes input

```
bc/cctv/00/cctv_0001   0    0              On    IN  (TOP(S(PP*      -    -   -   Speaker#1   *   (ARGM-LOC*     -
bc/cctv/00/cctv_0001   0    1               a    DT     (NP(NP*      -    -   -   Speaker#1   *            *     -
bc/cctv/00/cctv_0001   0    2            wall    NN           *)   wall   -   -   Speaker#1   *            *     -
bc/cctv/00/cctv_0001   0    3         outside    IN        (PP*      -    -   -   Speaker#1   *            *     -
bc/cctv/00/cctv_0001   0    4             the    DT        (NP*      -    -   -   Speaker#1   *            *     -
bc/cctv/00/cctv_0001   0    5    headquarters    NN        *))))     -    -   -   Speaker#1   *            *)    -
bc/cctv/00/cctv_0001   0    6              we   PRP        (NP*)     -    -   -   Speaker#1   *       (ARG0*)    -
bc/cctv/00/cctv_0001   0    7           found   VBD        (VP*    find  01   1   Speaker#1   *          (V*)    -
bc/cctv/00/cctv_0001   0    8               a    DT        (NP*      -    -   -   Speaker#1   *       (ARG1*   (61
bc/cctv/00/cctv_0001   0    9             map    NN          *))    map   -   -   Speaker#1   *            *)   61)
bc/cctv/00/cctv_0001   0   10               .     .          *))     -    -   -   Speaker#1   *            *     -

bc/cctv/00/cctv_0001   0    0             This    DT  (TOP(S(NP*      -    -   -   Speaker#1       *   (ARG1*   (61
bc/cctv/00/cctv_0001   0    1              map    NN           *)    map   -   -   Speaker#1       *        *)   61)
bc/cctv/00/cctv_0001   0    2              was   VBD        (VP*      be  01   2   Speaker#1       *      (V*)    -
bc/cctv/00/cctv_0001   0    3              the    DT  (NP(NP(NP*      -    -   -   Speaker#1   (ORG*   (ARG2*   (36
bc/cctv/00/cctv_0001   0    4           Eighth   NNP       (NML*      -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0    5            Route   NNP           *)     -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0    6             Army   NNP           *      -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0    7               's   POS           *)     -    -   -   Speaker#1       *)       *    36)
bc/cctv/00/cctv_0001   0    8        depiction    NN           *)     -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0    9               of    IN        (PP*      -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0   10              the    DT     (NP(NP*      -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0   11    Mediterranean   NNP       (NML*      -    -   -   Speaker#1   (LOC*        *     -
bc/cctv/00/cctv_0001   0   12              Sea   NNP           *)     -    -   -   Speaker#1       *)       *     -
bc/cctv/00/cctv_0001   0   13        situation    NN           *)     -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0   14               at    IN        (PP*      -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0   15             that    DT        (NP*      -    -   -   Speaker#1       *        *     -
bc/cctv/00/cctv_0001   0   16             time    NN      *))))))   time   -   -   Speaker#1       *        *)    -
bc/cctv/00/cctv_0001   0   17                .     .          *))     -    -   -   Speaker#1       *        *     -

```


### Example OntoNotes output

```
sentence	has_det	is_coref	string	pos_string	head	pos_head	core	pos_core	mod	pos_mod	unigram_pre	pos_unigram_pre	bigram_pre	pos_bigram_pre	trigram_pre	pos_trigram_pre	unigram_post	pos_unigram_post	bigram_post	pos_bigram_post	trigram_post	pos_trigram_post
On a wall outside the headquarters we found a map . 	True	False	_wall_	_NN_	wall	NN	_wall_	_NN_	_	_	_BOS_	_BOS_	_BOS_BOS	_BOS_BOS	_BOS_BOS_BOS	_BOS_BOS_BOS	_the_	_DT_	_the_we_	_DT_PRP_	_the_we_a_	_DT_PRP_DT_
On a wall outside the headquarters we found a map . 	True	False	_headquarters_	_NN_	headquarters	NN	_headquarters_	_NN_	_	_	_wall_	_NN_	_On_wall_	_IN_NN_	_BOS_On_wall_	_BOS_IN_NN_	_found_	_VBD_	_found_map_	_VBD_NN_	_found_map_EOS_	_VBD_NN_EOS_
On a wall outside the headquarters we found a map . 	True	False	_map_	_NN_	map	NN	_map_	_NN_	_	_	_we_	_PRP_	_the_we_	_DT_PRP_	_wall_the_we_	_NN_DT_PRP_	_EOS_	_EOS_	_EOS_EOS	_EOS_EOS	_EOS_EOS_EOS	_EOS_EOS_EOS
This map was the Eighth Route Army 's depiction of the Mediterranean Sea situation at that time . 	True	True	_map_	_NN_	map	NN	_map_	_NN_	_	_	_BOS_	_BOS_	_BOS_BOS	_BOS_BOS	_BOS_BOS_BOS	_BOS_BOS_BOS	_the_	_DT_	_the_Route_	_DT_NNP_	_the_Route_'s_	_DT_NNP_POS_
This map was the Eighth Route Army 's depiction of the Mediterranean Sea situation at that time . 	True	False	_Eighth_Route_Army_	_NNP_NNP_NNP_	Army	NNP	_Eighth_Route_Army_	_NNP_NNP_NNP_	_	_	_map_	_NN_	_BOS_map_	_BOS_NN_	_BOS_BOS_map_	_BOS_BOS_NN_	_depiction_	_NN_	_depiction_the_	_NN_DT_	_depiction_the_Sea_	_NN_DT_NNP_
This map was the Eighth Route Army 's depiction of the Mediterranean Sea situation at that time . 	False	False	_'s_depiction_	_POS_NN_	depiction	NN	_depiction_	_NN_	_'s_	_POS_	_Route_	_NNP_	_the_Route_	_DT_NNP_	_map_the_Route_	_NN_DT_NNP_	_the_	_DT_	_the_Sea_	_DT_NNP_	_the_Sea_at_	_DT_NNP_IN_
This map was the Eighth Route Army 's depiction of the Mediterranean Sea situation at that time . 	True	False	_Mediterranean_Sea_situation_	_NNP_NNP_NN_	situation	NN	_Mediterranean_Sea_situation_	_NNP_NNP_NN_	_	_	_depiction_	_NN_	_Army_depiction_	_NNP_NN_	_Eighth_Army_depiction_	_NNP_NNP_NN_	_that_	_DT_	_that_._	_DT_._	_that_._EOS_	_DT_._EOS_
This map was the Eighth Route Army 's depiction of the Mediterranean Sea situation at that time . 	True	False	_time_	_NN_	time	NN	_time_	_NN_	_	_	_situation_	_NN_	_Mediterranean_situation_	_NNP_NN_	_of_Mediterranean_situation_	_IN_NNP_NN_	_EOS_	_EOS_	_EOS_EOS	_EOS_EOS	_EOS_EOS_EOS	_EOS_EOS_EOS
```