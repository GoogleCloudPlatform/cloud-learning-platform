import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleTemplateComponent } from './single-template.component';

describe('SingleTemplateComponent', () => {
  let component: SingleTemplateComponent;
  let fixture: ComponentFixture<SingleTemplateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SingleTemplateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SingleTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
