#!/bin/bash

DATABASE=/home/mersmann/gsoc/datasets/study_package/iPRG2016.fasta
DATABASE_DECOY=/home/mersmann/gsoc/datasets/study_package/iPRG2016_decoy.fasta
INI=/home/mersmann/gsoc/ini_files
EXE=/home/mersmann/gsoc/THIRDPARTY/Linux/64bit
SCRIPTS=/home/mersmann/gsoc/analysis

SEARCH_ENGINE=$1
IN_FILE=$2
OUT_DIR=$3

BASE=$(basename $IN_FILE .mzML)
OUT=${OUT_DIR}/${BASE}

if [ $SEARCH_ENGINE == xtandem ]; then
	echo XTandemAdapter for targets ...
	XTandemAdapter -ini ${INI}/XTandemAdapter.ini -xtandem_executable ${EXE}/XTandem/tandem.exe -precursor_mass_tolerance 15 -database $DATABASE -in $IN_FILE -out ${OUT}_${SEARCH_ENGINE}_target.idXML

	echo XTandemAdapter for decoys ...
	XTandemAdapter -ini ${INI}/XTandemAdapter.ini -xtandem_executable ${EXE}/XTandem/tandem.exe -precursor_mass_tolerance 15 -database $DATABASE_DECOY -in $IN_FILE -out ${OUT}_${SEARCH_ENGINE}_decoy.idXML

elif [ $SEARCH_ENGINE == comet ]; then
	echo CometAdapter for targets ...
	CometAdapter -ini ${INI}/CometAdapter.ini -comet_executable ${EXE}/Comet/comet.exe -precursor_mass_tolerance 15 -allowed_missed_cleavages 1 -num_hits 1 -database $DATABASE -in $IN_FILE -out ${OUT}_${SEARCH_ENGINE}_target.idXML -pin_out ${OUT}_${SEARCH_ENGINE}_target_pin.csv

	echo CometAdapter for decoys ...
	CometAdapter -ini ${INI}/CometAdapter.ini -comet_executable ${EXE}/Comet/comet.exe -precursor_mass_tolerance 15 -allowed_missed_cleavages 1 -num_hits 1 -database $DATABASE_DECOY -in $IN_FILE -out ${OUT}_${SEARCH_ENGINE}_decoy.idXML -pin_out ${OUT}_${SEARCH_ENGINE}_decoy_pin.csv

elif [ $SEARCH_ENGINE == msgf ]; then
	echo MSGFPlusAdapter for targets ...
	MSGFPlusAdapter -ini ${INI}/MSGFPlusAdapter.ini -executable /home/mersmann/gsoc/THIRDPARTY/All/MSGFPlus/MSGFPlus.jar -precursor_mass_tolerance 15 -isotope_error_range 0,0 -fragment_method HCD -instrument high_res -database $DATABASE -in $IN_FILE -out ${OUT}_${SEARCH_ENGINE}_target.idXML

	echo MSGFPlusAdapter for decoys ...
	MSGFPlusAdapter -ini ${INI}/MSGFPlusAdapter.ini -executable /home/mersmann/gsoc/THIRDPARTY/All/MSGFPlus/MSGFPlus.jar -precursor_mass_tolerance 15 -isotope_error_range 0,0 -fragment_method HCD -instrument high_res -database $DATABASE_DECOY -in $IN_FILE -out ${OUT}_${SEARCH_ENGINE}_decoy.idXML

else
	echo valid search engines: xtandem / msgf / comet
fi

echo IDPosteriorErrorProbability ...
IDPosteriorErrorProbability -ini ${INI}/IDPosteriorErrorProbability.ini -in ${OUT}_${SEARCH_ENGINE}_target.idXML -out ${OUT}_${SEARCH_ENGINE}_target_IDPEP.idXML
	
echo PSMFeatureExtractor for targets ...
PSMFeatureExtractor -ini ${INI}/PSMFeatureExtractor.ini -in ${OUT}_${SEARCH_ENGINE}_target.idXML -out ${OUT}_${SEARCH_ENGINE}_target_features.idXML

echo PSMFeatureExtractor for decoys ...
PSMFeatureExtractor -ini ${INI}/PSMFeatureExtractor.ini -in ${OUT}_${SEARCH_ENGINE}_decoy.idXML -out ${OUT}_${SEARCH_ENGINE}_decoy_features_raw.idXML

if [ $SEARCH_ENGINE == msgf ]; then
	python ${SCRIPTS}/annotate_idXML_with_target_decoy_info.py ${OUT}_${SEARCH_ENGINE}_decoy_features_raw.idXML ${OUT}_${SEARCH_ENGINE}_decoy_features.idXML
fi

for THRESH in 0.01 0.05; do

	echo PercolatorAdapter at ${THRESH} ...
	PercolatorAdapter -ini ${INI}/PercolatorAdapter.ini -percolator_executable ${EXE}/Percolator/percolator -trainFDR $THRESH -testFDR $THRESH -out ${OUT}_${SEARCH_ENGINE}_features_percolator_F${THRESH}_t${THRESH}.idXML -in ${OUT}_${SEARCH_ENGINE}_target_features.idXML -in_decoy ${OUT}_${SEARCH_ENGINE}_decoy_features.idXML

done
