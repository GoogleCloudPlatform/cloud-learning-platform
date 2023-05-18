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
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { SectionComponent } from './section/section.component';
import { CreateSectionComponent } from './create-section/create-section.component';
// import { BrowserModule } from '@angular/platform-browser';
// import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatLegacyChipsModule as MatChipsModule } from '@angular/material/legacy-chips';
import { EditSectionComponent } from './edit-section/edit-section.component';
import { SectionListComponent } from './section-list/section-list.component';
import { DeleteOverviewDialog } from './section/section.component';
import { SuccessOverviewDialog } from './home.component';
import { CourseTemplateDetailsDialog } from './home.component';
import { InviteStudentModalComponent } from './invite-student-modal/invite-student-modal.component';
import { SingleTemplateComponent } from './single-template/single-template.component';
import { ViewLtiAssignmentDialog } from './single-template/single-template.component';
import { DeleteLtiDialog } from './single-template/single-template.component';
import { ViewSectionLtiAssignmentDialog } from './section/section.component';
import { DeleteSectionLtiDialog } from './section/section.component';

@NgModule({
  declarations: [
    HomeComponent,
    CohortComponent,
    ShowMoreComponent,
    CreateCohortModalComponent,
    CreateCourseTemplateModalComponent,
    CourseTemplateComponent,
    SectionComponent,
    CreateSectionComponent,
    EditSectionComponent,
    SectionListComponent,
    DeleteOverviewDialog,
    SuccessOverviewDialog,
    CourseTemplateDetailsDialog,
    InviteStudentModalComponent,
    SingleTemplateComponent,
    ViewLtiAssignmentDialog,
    DeleteLtiDialog,
    ViewSectionLtiAssignmentDialog,
    DeleteSectionLtiDialog
  ],
  // entryComponents: [CreateCohortModalComponent],
  imports: [
    CommonModule,
    // BrowserModule,
    // BrowserAnimationsModule,
    HomeRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    SharedModule,
    MaterialSharedModule,
    MatChipsModule,
    NgxSkeletonLoaderModule.forRoot({ animation: 'progress' })

  ],
  providers: [

  ]
})
export class HomeModule { }
