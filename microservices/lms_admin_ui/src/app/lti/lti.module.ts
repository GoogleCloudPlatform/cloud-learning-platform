import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToolsListComponent } from './tools-list/tools-list.component';
import { ToolFormComponent } from './tool-form/tool-form.component';
import { SharedModule } from '../shared/shared.module';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { ReactiveFormsModule } from '@angular/forms';
import { MaterialSharedModule } from '../shared/material-shared.module';
import { LtiRoutingModule } from './lti-routing.module';

@NgModule({
  declarations: [
    ToolsListComponent,
    ToolFormComponent
  ],
  imports: [
    CommonModule,
    LtiRoutingModule,
    SharedModule,
    MaterialSharedModule,
    ReactiveFormsModule,
    NgxSkeletonLoaderModule.forRoot({ animation: 'progress' })
  ]
})
export class LtiModule { }
