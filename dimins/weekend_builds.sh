#!/bin/sh

SCRIPT_DIR=/DI_San/projects/reports/weekend_builds/
     
#the newest models should be no more than $DAYS old...
DAYS=5

cd ${SCRIPT_DIR} || exit 1


#list of emails to send the report
EMAILS=(
    spowers@dimins.com
    johns@dimins.com
    Dick.Walker@pernod-ricard-usa.com
    Matt.Key@pernod-ricard-usa.com
    Philip.Perez@pernod-ricard-usa.com
)
#list of directories to monitor
directories=(
    /di_atlantis/dl-dataroot/data/wine_comp
    /di_atlantis/dl-dataroot/data/mandates
    /di_atlantis/dl-dataroot/data/bottles_reports
    /di_atlantis/dl-dataroot/data/same_store/models
)


LOGFILE=builds.txt

#EMAILS=$(list_emails | tr '\n' ' ')

function recent_model_check() {
    DIR=$1
    find ${DIR}/ -name "*.mdl" -mtime -${DAYS} | grep . >/dev/null
    return $?
}


for d in ${directories[@]}; do
    
    #print the directory's status
    if recent_model_check $d;  
        then echo -ne "STATUS: OKAY\t"
        else echo -ne "STATUS: WARNING\t"
    fi

    #print the total size of the directory
    echo -ne "$d\t"
    du -sh $d/|cut -f1 

    echo #spacing

    #print the newest 4 models
    ( cd $d && find . -name "*.mdl" -printf "%TY-%Tm-%Td %Tr\t%h/%f\n" | sort -nr | head -n4 )

    echo #spacing

done > "${LOGFILE}"





count=$(grep -c "STATUS: OKAY" "${LOGFILE}")
if [ "$count" -eq 4 ];
    then SUBJECT="Weekend builds successful";
    else SUBJECT="${count}/4 weekend builds succesful";
fi

cp "${LOGFILE}" logs/builds.$(date +%F).txt
mail -s "${SUBJECT}" "${EMAILS}" < "${LOGFILE}"

