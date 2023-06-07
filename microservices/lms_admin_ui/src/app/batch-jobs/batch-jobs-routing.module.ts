import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BatchJobsListComponent } from './batch-jobs-list/batch-jobs-list.component';

const routes: Routes = [
  {
    path: '',
    component: BatchJobsListComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobsRoutingModule { }
