import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SectionListComponent } from './section-list.component';
import { By } from '@angular/platform-browser';

describe('SectionListComponent', () => {
  let component: SectionListComponent;
  let fixture: ComponentFixture<SectionListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SectionListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SectionListComponent);
    component = fixture.componentInstance;
    const expectedList = [       {
      "id": "5lUaIj8fP4cS8jZcEk",
      "name": "JWT_test2",
      "section": "test section",
      "description": "testing",
      "classroom_id": "6131026561",
      "classroom_code": "afhn75",
      "classroom_url": "https://classroom.google.com/c/NjEzMTNTI2NTYx",
      "course_template": "course_templates/fHI8HdbWACPXsj5w2Y",
      "cohort": "cohorts/qhDMJeG3BYNe6l6TG6",
      "status": "FAILED_TO_PROVISION",
      "enrollment_status": "CLOSED",
      "enrolled_students_count": 0,
      "max_students": 2
  }]
    component.sectionList = expectedList
    fixture.detectChanges();
  });

  

  it('should create', () => {
    expect(component).toBeTruthy();
  });


  it('should have section rendered', async() => {
    fixture.whenStable()
    fixture.detectChanges();
    const debugTaskTitle = fixture.debugElement.queryAll(By.css('div.data-obj-card'))      
    expect(debugTaskTitle.length).toBeGreaterThan(0)
  })


  it('should have a section title as test section', ()=>{
    fixture.detectChanges();
    const titleText = 'test section'
    const titleElement = fixture.debugElement.query(By.css('.title > .text'))
    expect(titleElement.nativeElement.textContent).toBe(titleText)
  })

  
  it('should have a metadata as JWT_test2', ()=>{
    fixture.detectChanges();
    const metaText = 'JWT_test2'
    const metaElement = fixture.debugElement.query(By.css('.metadata  .body'))
    expect(metaElement.nativeElement.textContent).toBe(metaText)
  })

});
