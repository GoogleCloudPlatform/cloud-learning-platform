import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LmsJobsListComponent } from './lms-jobs-list/lms-jobs-list.component';

const routes: Routes = [
  {
    path: '',
    component: LmsJobsListComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobsRoutingModule { }
