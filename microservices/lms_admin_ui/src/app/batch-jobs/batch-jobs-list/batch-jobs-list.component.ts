import { Component, ViewChild, Inject } from '@angular/core';
import { MatLegacyTableDataSource as MatTableDataSource } from '@angular/material/legacy-table'
import { MatSort } from '@angular/material/sort';
import { JobsService } from '../service/batch-jobs.service';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { PageEvent } from '@angular/material/paginator';


interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-batch-jobs-list',
  templateUrl: './batch-jobs-list.component.html',
  styleUrls: ['./batch-jobs-list.component.scss']
})
export class BatchJobsListComponent {
  isLoadingData: boolean = true
  batchJobsData = []
  jobSkip: number = 0
  jobLimit: number = 10
  jobPageSize: number = 10
  paginator: PageEvent;

  dataSource = new MatTableDataSource(this.batchJobsData);

  batchJobDisplayedColumns: string[] = ['id', 'job_type', 'section_id', 'classroom_id', 'created_time', 'start_time', 'end_time', 'status', 'input_data', 'logs'];

  constructor(public dialog: MatDialog, private JobsService: JobsService) { }
  @ViewChild(MatSort) sort: MatSort;

  ngOnInit(): void {
    this.dataSource.sort = this.sort;
    this.fetchJobs()
  }

  handleBatchJobPageEvent(e: PageEvent) {
    this.paginator = e;

    if (this.paginator.pageSize != this.jobPageSize) {
      this.jobSkip = 0
      this.jobLimit = this.paginator.pageSize
      this.jobPageSize = this.paginator.pageSize
    }
    else {
      if (this.paginator.pageIndex > this.paginator.previousPageIndex) {
        this.jobSkip = this.jobLimit
        this.jobLimit = this.jobLimit + this.paginator.pageSize
      }
      else if (this.paginator.previousPageIndex > this.paginator.pageIndex) {
        this.jobSkip = this.jobSkip - this.paginator.pageSize
        this.jobLimit = this.jobLimit - this.paginator.pageSize
      }
    }
    console.log("skip ", this.jobSkip, 'limit ', this.jobLimit)
    this.fetchJobs()
  }

  fetchJobs() {
    this.isLoadingData = true
    this.JobsService.getJobsList(this.jobSkip, this.jobLimit).subscribe((response: any) => {
      setTimeout(() => {
        this.isLoadingData = false
      }, 100);
      if (response.success == true) {
        this.batchJobsData = response.data
        console.log("batchJobsData", this.batchJobsData)
      }
      else {
        console.log("response", response?.message)
      }
    })
  }

  openViewLogsDialog(data): void {
    console.log("data", data)
    let jobLogs: LooseObject = {}
    jobLogs['mode'] = 'View'
    jobLogs['init_data'] = ''
    jobLogs['data'] = { ...data }

    const dialogRef = this.dialog.open(ViewJobLogDialog, {
      width: '80vw',
      maxWidth: '900px',
      maxHeight: "90vh",
      data: jobLogs
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
    });
  }

  openViewInputDataDialog(data): void {
    console.log("data", data)
    let inputData: LooseObject = {}
    inputData['mode'] = 'View'
    inputData['init_data'] = ''
    inputData['data'] = { ...data }

    const dialogRef = this.dialog.open(ViewInputDataDialog, {
      width: '80vw',
      maxWidth: '900px',
      maxHeight: "90vh",
      data: inputData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
    });
  }

}

@Component({
  selector: 'view-batch-job-log-dialog',
  templateUrl: 'view-batch-job-log-dialog.html',
  styleUrls: ['batch-jobs-list.component.scss']
})
export class ViewJobLogDialog {
  logData: any;
  objectKeys = Object.keys
  constructor(
    public dialogRef: MatDialogRef<ViewJobLogDialog>,
    @Inject(MAT_DIALOG_DATA) public viewDialogData: any, public JobsService: JobsService
  ) {
    this.logData = viewDialogData.data
    console.log("log data", this.logData)
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }
}


@Component({
  selector: 'view-input-data-dialog',
  templateUrl: 'view-batch-job-input-data-dialog.html',
  styleUrls: ['batch-jobs-list.component.scss']
})
export class ViewInputDataDialog {
  inputData: any;
  objectKeys = Object.keys
  constructor(
    public dialogRef: MatDialogRef<ViewInputDataDialog>,
    @Inject(MAT_DIALOG_DATA) public viewDialogData: any, public JobsService: JobsService
  ) {
    this.inputData = viewDialogData.data
    console.log("input data", this.inputData)
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}

@Component({
  selector: 'keyvalue-pipe',
  template: ``
})
export class KeyValuePipeComponent {
  object: { [key: number]: string } = { 2: 'foo', 1: 'bar' };
  map = new Map([[2, 'foo'], [1, 'bar']]);
}