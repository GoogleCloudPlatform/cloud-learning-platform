import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home.component';
import { HomeRoutingModule } from './home-routing.module';
import { CohortComponent } from './cohort/cohort.component';
import { SharedModule } from '../shared/shared.module';
import { MaterialSharedModule } from '../shared/material-shared.module';
import { ShowMoreComponent } from './show-more/show-more.component';
import { CreateCohortModalComponent } from './create-cohort-modal/create-cohort-modal.component';
import { CreateCourseTemplateModalComponent } from './create-course-template-modal/create-course-template-modal.component';
import { CourseTemplateComponent } from './course-template/course-template.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader'

@NgModule({
  declarations: [
    HomeComponent,
    CohortComponent,
    ShowMoreComponent,
    CreateCohortModalComponent,
    CreateCourseTemplateModalComponent,
    CourseTemplateComponent,

  ],
  // entryComponents: [CreateCohortModalComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    ReactiveFormsModule,
    SharedModule,
    MaterialSharedModule,
    NgxSkeletonLoaderModule.forRoot({ animation: 'progress' })

  ],
  providers: [

  ]
})
export class HomeModule { }
