import { HomeComponent } from './home.component';
import { SectionComponent } from './section/section.component';

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SingleTemplateComponent } from './single-template/single-template.component';

const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
    },
    {
        path: 'course-template/:id',
        component: SingleTemplateComponent,
    },
    {
        path: ':id',
        component: SectionComponent,
    },
    {
        path: ':id/:id',
        component: SectionComponent,
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class HomeRoutingModule { }