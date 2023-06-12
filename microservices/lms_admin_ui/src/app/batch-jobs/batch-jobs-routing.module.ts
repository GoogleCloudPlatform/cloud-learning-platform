import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LmsJobsListComponent } from './batch-jobs-list/batch-jobs-list.component';

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
