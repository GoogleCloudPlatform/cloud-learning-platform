import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LmsJobsListComponent } from './lms-jobs-list/lms-jobs-list.component';
import { SharedModule } from '../shared/shared.module';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { ReactiveFormsModule } from '@angular/forms';
import { MaterialSharedModule } from '../shared/material-shared.module';
import { JobsRoutingModule } from './lms-jobs-routing.module';
import { ViewJobLogDialog } from './lms-jobs-list/lms-jobs-list.component';
import { ViewInputDataDialog } from './lms-jobs-list/lms-jobs-list.component';

@NgModule({
  declarations: [
    LmsJobsListComponent,
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
