import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CohortComponent } from './cohort.component';
import { Router } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { By } from '@angular/platform-browser';
describe('CohortComponent', () => {
  
  let component: CohortComponent;
  let fixture: ComponentFixture<CohortComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, MatMenuModule, ],
      declarations: [ CohortComponent ],
      providers: [MatDialog, Router]
    })
    .compileComponents();
    fixture = TestBed.createComponent(CohortComponent);
    component = fixture.componentInstance;
    const tempCohortList = [{
      course_template: "course_templates/fHI8Hdb8WAACPXsj5w2Y",
      course_template_name: "JWT_test2",
      description: "this is description",
      end_date: "2023-05-10T00:00:00+00:00",
      enrolled_students_count: 2,
      id: "qhDMJeG3BNYNme6l6TG6",
      max_students: 200,
      name: "Jwt test2",
      registration_end_date: "2023-06-30T00:00:00+00:00",
      registration_start_date: "2023-05-30T00:00:00+00:00",
      start_date: "2023-05-14T00:00:00+00:00"
    }]
    component.cohortList = tempCohortList
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should click options button of first cohort',()=>{
    const onClickMock = spyOn(component, 'setSelected');
    const cohortElements = fixture.debugElement.queryAll(By.css('.data-obj-card'))
    const moreElement = cohortElements[0].query(By.css('.more-options .material-symbols-rounded'))
    moreElement.triggerEventHandler('click',null)
    fixture.detectChanges()
    expect(onClickMock).toHaveBeenCalled()
  })

  it('should click first options button and select first cohort',async()=>{
    const cohortElements = fixture.debugElement.queryAll(By.css('.data-obj-card'))
    const moreElement = cohortElements[0].query(By.css('.more-options .material-symbols-rounded'))
    moreElement.nativeElement.click()
    fixture.detectChanges()
    expect(component.selectedCohort).toEqual(component.cohortList[0])
  })

  it('should check first enrolled to be greater than 0',()=>{
    const cohortElements = fixture.debugElement.queryAll(By.css('.data-obj-card'))
    const enrollElement = cohortElements[0].query(By.css('.enrolled-section .number'))
    expect(Number(enrollElement.nativeElement.textContent)).toEqual(component.cohortList[0].enrolled_students_count)
  })


});

