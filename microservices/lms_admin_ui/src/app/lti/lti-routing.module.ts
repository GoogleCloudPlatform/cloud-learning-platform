import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ToolsListComponent } from './tools-list/tools-list.component';
import { CreateAssignmentComponent } from './create-assignment/create-assignment.component';

const routes: Routes = [
  // {
  //   path: '',
  //   component: CreateAssignmentComponent
  // },
  {
    path: '',
    component: ToolsListComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LtiRoutingModule { }
