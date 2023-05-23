import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToolsListComponent } from './tools-list/tools-list.component';
import { ToolFormComponent } from './tool-form/tool-form.component';
import { SharedModule } from '../shared/shared.module';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { ReactiveFormsModule } from '@angular/forms';
import { MaterialSharedModule } from '../shared/material-shared.module';
import { LtiRoutingModule } from './lti-routing.module';
import { CreateAssignmentComponent } from './create-assignment/create-assignment.component';
import { ContentSelectorComponent } from './content-selector/content-selector.component';
import { ViewLtiDialog } from './tools-list/tools-list.component';
import { DeleteLtiDialog } from './tools-list/tools-list.component';

@NgModule({
  declarations: [
    ToolsListComponent,
    ToolFormComponent,
    CreateAssignmentComponent,
    ContentSelectorComponent,
    ViewLtiDialog,
    DeleteLtiDialog
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
