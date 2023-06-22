import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BreadcrumComponent } from './breadcrum.component';
import {} from 'jasmine';
import { By } from '@angular/platform-browser';

describe('BreadcrumComponent', () => {
  let component: BreadcrumComponent;
  let fixture: ComponentFixture<BreadcrumComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BreadcrumComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BreadcrumComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('Should have home breadcrumb', () =>{ 
    const breadcrumbText = 'Home /'
    fixture.detectChanges();
    const span = fixture.debugElement.query(By.css('.text'));
    expect(span.nativeElement.textContent.trim()).toBe(breadcrumbText)
  })
});
