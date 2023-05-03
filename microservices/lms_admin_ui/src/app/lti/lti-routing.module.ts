import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ToolsListComponent } from './tools-list/tools-list.component';

const routes: Routes = [
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
