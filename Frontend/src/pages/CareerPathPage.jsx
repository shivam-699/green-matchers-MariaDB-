import { useState } from 'react';
import CareerPath from '../components/CareerPath';

const CareerPathPage = () => {
  return (
    <div className="max-w-6xl mx-auto w-full space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">Career Path Explorer</h1>
        <p className="text-slate-300 text-lg">
          Discover your growth trajectory in sustainable careers
        </p>
      </div>

      {/* Career Path Component */}
      <CareerPath />

      {/* Additional Insights */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="glass-premium rounded-2xl p-6">
          <div className="text-3xl mb-4">📚</div>
          <h3 className="text-xl font-bold text-white mb-3">Skill Development</h3>
          <ul className="text-slate-300 space-y-2">
            <li>• Advanced Python for Sustainability</li>
            <li>• ESG Reporting Frameworks</li>
            <li>• Renewable Energy Analytics</li>
            <li>• Carbon Accounting Methods</li>
          </ul>
        </div>

        <div className="glass-premium rounded-2xl p-6">
          <div className="text-3xl mb-4">🏆</div>
          <h3 className="text-xl font-bold text-white mb-3">Certifications</h3>
          <ul className="text-slate-300 space-y-2">
            <li>• LEED Green Associate</li>
            <li>• ESG Analyst Certification</li>
            <li>• Sustainable Development Goals</li>
            <li>• Carbon Management Professional</li>
          </ul>
        </div>
      </div>

      {/* Market Insights */}
      <div className="glass-premium rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="text-2xl">💡</div>
          <h3 className="text-xl font-bold text-white">Market Insights</h3>
        </div>
        <div className="grid md:grid-cols-3 gap-4 text-slate-300">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">+32%</div>
            <div className="text-sm">Green Job Growth</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">₹15-25L</div>
            <div className="text-sm">Average Salary Range</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">500+</div>
            <div className="text-sm">Companies Hiring</div>
          </div>
        </div>
      </div>

      {/* Success Stories */}
      <div className="glass-premium rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="text-2xl">🌟</div>
          <h3 className="text-xl font-bold text-white">Success Stories</h3>
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-slate-800/50 rounded-xl p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold">
                AS
              </div>
              <div>
                <div className="text-white font-semibold">Aisha Sharma</div>
                <div className="text-green-400 text-sm">Solar Engineer → Team Lead</div>
              </div>
            </div>
            <p className="text-slate-300 text-sm">
              "Green Matchers helped me transition from traditional engineering to renewable energy with a 45% salary increase in 2 years."
            </p>
          </div>
          <div className="bg-slate-800/50 rounded-xl p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-teal-600 rounded-xl flex items-center justify-center text-white font-bold">
                RK
              </div>
              <div>
                <div className="text-white font-semibold">Rohan Kumar</div>
                <div className="text-green-400 text-sm">Data Analyst → ESG Director</div>
              </div>
            </div>
            <p className="text-slate-300 text-sm">
              "The career path guidance and skill mapping transformed my career trajectory in sustainability analytics."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CareerPathPage;