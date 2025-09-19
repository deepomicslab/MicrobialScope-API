import os
import pandas as pd
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from analysis.models import Task

FILE_PATH = 'C:\\Users\\Paranoid\\Desktop\\tasks.txt'

if __name__ == '__main__':
    df = pd.read_csv(FILE_PATH, sep='|')

    for _, row in df.iterrows():
        task = Task(
            name=row['name'],
            user=row['user'],
            uploadpath=row['uploadpath'],
            analysis_type=row['analysis_type'],
            modulelist=row['modulelist'],
            status=row['status'],
            task_log=row['task_log'],
            task_detail=row['task_detail'],
            created_at=row['created_at'],
            microbial_type=row['microbial_type']
        )

        task.save()


