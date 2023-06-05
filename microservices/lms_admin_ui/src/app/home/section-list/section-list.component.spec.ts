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
    const expectedList = [{
      'id':1,
      'section':'saurav section',
      'cohort': 'A',
      'classroom_url':'http://abc.com',
      'description':'ABC',
      'name':'Test LTI'
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


  it('should have a section title as Saurav Section', ()=>{
    fixture.detectChanges();
    const titleText = 'saurav section'
    const titleElement = fixture.debugElement.query(By.css('.title > .text'))
    expect(titleElement.nativeElement.textContent).toBe(titleText)
  })

  
  it('should have a metadata as Test LTI', ()=>{
    fixture.detectChanges();
    const metaText = 'Test LTI'
    const metaElement = fixture.debugElement.query(By.css('.metadata  .body'))
    expect(metaElement.nativeElement.textContent).toBe(metaText)
  })

});
