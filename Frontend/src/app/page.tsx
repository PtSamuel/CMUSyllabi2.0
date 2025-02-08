'use client';

import * as React from 'react';
import '@/lib/env';

import Button from '@/components/buttons/Button';
import { LinkIcon, SearchIcon } from 'lucide-react';
import UnderlineLink from '@/components/links/UnderlineLink';


interface T_CourseEntry {
  category: "PDF" | "HTML" | "Unknown";
  course_number: string;
  department: string;
  semester: string;
  syllabus_href: string;
};


function CourseEntry({ course_number, department, semester, syllabus_href }: T_CourseEntry) {
  return (
    <li className='bg-white border border-slate-200 rounded-md p-4 my-4'>
      <div className='flex flex-row flex-nowrap justify-between'>

      <h2 className='text-lg font-normal'>
        {course_number} &nbsp;
        <span className='rounded-full bg-primary-100 px-2 py-1 text-primary-700 font-normal text-sm'>{semester}</span>
      </h2>
      <UnderlineLink href={syllabus_href}><LinkIcon size={16} className='mr-2'/> Syllabus Link</UnderlineLink>
      </div>
    </li>
  );
}


export default function HomePage() {
  const [search, setSearch] = React.useState<string>('');
  const [results, setResults] = React.useState<T_CourseEntry[]>([]);
  const [semester, setSemester] = React.useState<Set<string>>(new Set());

  const searchSyllabus = async (search: string) => {
    const res = await fetch(`http://3.230.154.38:3000/api/find_course?course_number=${search}`);
    const data = await res.json();
    if (data.length === undefined) {
      setResults([]);
      return;
    }
    setResults(data);
    setSemester(new Set());
  };

  const AllSemesters = new Set(results.map(value => value.semester));

  return (
    <main className='bg-white layout my-4'>
      <div>
        <h1 className='text-3xl font-semibold'>Syllabus Searcher</h1>
 
        <div className='flex flex-row flex-nowrap space-x-4 mt-4'>
          <div className="w-full max-w-sm min-w-[200px]">
            <input 
              className="w-full bg-transparent placeholder:text-slate-400 text-slate-700 text-sm border border-slate-200 rounded-md px-3 py-2 transition duration-300 ease focus:outline-none focus:border-slate-400 hover:border-slate-300 shadow-sm focus:shadow"
              placeholder="Course Number"
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>


          <Button leftIcon={SearchIcon} onClick={() => searchSyllabus(search)}>Search</Button>
        </div>
        <div className='flex flex-row flex-wrap mt-4 items-baseline'>
          <span className='text-slate-500 mr-2'>{AllSemesters.size > 0 ? "Semesters:" : ""}</span>
          {Array.from(AllSemesters).map((s, index) => (
            semester.has(s) ? 
            <button key={index} 
            className='rounded-full bg-primary-500 border-primary-800 border-2 px-2 py-1 text-primary-100 font-normal text-sm mr-2 hover:bg-primary-200'
            onClick={() => setSemester(
              sems => {
                sems.delete(s);
                return new Set(sems);
              }
            )}>{s}</button>
            :
            <button key={index} 
            className='rounded-full bg-white border-primary-400 border-2 px-2 py-1 text-primary-700 font-normal text-sm mr-2 hover:bg-primary-200'
            onClick={() => setSemester(
              sems => {
                sems.add(s);
                return new Set(sems);
              }
            )}>{s}</button>
          ))}
        </div>
      </div>

      <div>
        <ol>
          {results.filter(value => {
            if (semester.size === 0) return true;
            return semester.has(value.semester);
          }).map((result, index) => <CourseEntry key={index} {...result}/>)}
        </ol>
      </div>
    </main>
  );
}
