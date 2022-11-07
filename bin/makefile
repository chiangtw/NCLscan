ALL_TOOLS = \
	AssembleExons \
	AssembleFastq \
	FastqOut \
	GetInfo \
	GetKey \
	GetNameB4Dot \
	InsertInList \
	JSFilter \
	JSParser \
	JunctionSite2BED \
	PslChimeraFilter \
	RemoveInList \
	RetainInList \
	RmBadMapping \
	RmColinearPairInSam \
	RmRedundance \
	SeqOut

ALL_PY_TOOLS = \
	Add_read_count.py \
	AssembleJSeq.py \
	append_Z3_tag.py \
	create_reference.py \
	get_gene_name.py \
	mp_blat.py

all: $(ALL_TOOLS) py_scripts


AssembleExons: Common.o Table.o AssembleExons.o
	$(CXX) Common.o Table.o AssembleExons.o -o AssembleExons

AssembleFastq: Common.o Table.o Seq.o AssembleFastq.o
	$(CXX) Common.o Table.o Seq.o AssembleFastq.o -o AssembleFastq

FastqOut: Common.o Table.o Seq.o Map.o FastqOut.o
	$(CXX) Common.o Table.o Seq.o Map.o FastqOut.o -o FastqOut

GetInfo: Common.o Table.o Map.o GetInfo.o
	$(CXX) Common.o Table.o Map.o GetInfo.o -o GetInfo

GetKey: Common.o Table.o Map.o GetKey.o
	$(CXX) Common.o Table.o Map.o GetKey.o -o GetKey

GetNameB4Dot: Common.o Table.o GetNameB4Dot.o
	$(CXX) Common.o Table.o GetNameB4Dot.o -o GetNameB4Dot

InsertInList: Common.o Table.o Map.o InsertInList.o
	$(CXX) Common.o Table.o Map.o InsertInList.o -o InsertInList

JSFilter: Common.o Table.o Sam.o JSFilter.o
	$(CXX) Common.o Table.o Sam.o JSFilter.o -o JSFilter

JSParser: Common.o Table.o Sam.o JSParser.o
	$(CXX) Common.o Table.o Sam.o JSParser.o -o JSParser

JunctionSite2BED: Common.o Table.o Map.o Annotation.o JunctionSite2BED.o
	$(CXX) Common.o Table.o Map.o Annotation.o JunctionSite2BED.o -o JunctionSite2BED

PslChimeraFilter: Common.o Table.o PslChimeraFilter.o
	$(CXX) Common.o Table.o PslChimeraFilter.o -o PslChimeraFilter

RemoveInList: Common.o Table.o Map.o RemoveInList.o
	$(CXX) Common.o Table.o Map.o RemoveInList.o -o RemoveInList

RetainInList: Common.o Table.o Map.o RetainInList.o
	$(CXX) Common.o Table.o Map.o RetainInList.o -o RetainInList

RmBadMapping: Common.o Table.o RmBadMapping.o
	$(CXX) Common.o Table.o RmBadMapping.o -o RmBadMapping

RmColinearPairInSam: Common.o Table.o Sam.o RmColinearPairInSam.o
	$(CXX) Common.o Table.o Sam.o RmColinearPairInSam.o -o RmColinearPairInSam

RmRedundance: Common.o Table.o Map.o RmRedundance.o
	$(CXX) Common.o Table.o Map.o RmRedundance.o -o RmRedundance

SeqOut: Common.o Table.o Seq.o Map.o SeqOut.o
	$(CXX) Common.o Table.o Seq.o Map.o SeqOut.o -o SeqOut

py_scripts: $(ALL_PY_TOOLS)
	@chmod +x $(ALL_PY_TOOLS)

.PHONY: clean install uninstall

clean:
	$(RM) *.o $(ALL_TOOLS)

install:
	install $(ALL_TOOLS) $(ALL_PY_TOOLS) $(PREFIX)

uninstall:
	cd $(PREFIX); $(RM) $(ALL_TOOLS) $(ALL_PY_TOOLS)
