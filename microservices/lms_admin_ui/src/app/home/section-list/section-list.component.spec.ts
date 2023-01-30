import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SectionListComponent } from './section-list.component';

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
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
