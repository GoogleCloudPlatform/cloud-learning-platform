import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BatchJobsListComponent } from './batch-jobs-list/batch-jobs-list.component';
import { SharedModule } from '../shared/shared.module';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { ReactiveFormsModule } from '@angular/forms';
import { MaterialSharedModule } from '../shared/material-shared.module';
import { JobsRoutingModule } from './batch-jobs-routing.module';
import { ViewJobLogDialog } from './batch-jobs-list/batch-jobs-list.component';
import { ViewInputDataDialog } from './batch-jobs-list/batch-jobs-list.component';

@NgModule({
  declarations: [
    BatchJobsListComponent,
    ViewJobLogDialog,
    ViewInputDataDialog
  ],
  imports: [
    CommonModule,
    JobsRoutingModule,
    SharedModule,
    MaterialSharedModule,
    ReactiveFormsModule,
    NgxSkeletonLoaderModule.forRoot({ animation: 'progress' })
  ]
})
export class JobsModule { }
